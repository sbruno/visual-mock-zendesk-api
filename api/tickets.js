import { addJobResultToMemory, generateTicketId, getCurrentTimestamp, normalizeId } from "./helpers.js"
import { insertPersistedComment, insertPersistedTicket, insertPersistedUser, updatePersistedTicket, validateInternalTicket } from "./schema.js"
import assert from "assert";
import lodash from 'lodash'
import { getDefaultAdminId, getGlobalState, getGlobalStateCopy, saveGlobalState } from "../persist.js"
import { renderPendingJob } from "./jobresults.js"
import {  transformIncomingUserIntoInternal, usersSearchByEmailImpl } from "./users.js"
import { allowShortcutStringComment, transformIncomingCommentIntoInternal } from "./comments.js"
import { runTriggersOnNewCommentPosted } from "./triggers.js"
import { intCustomFields } from "./customfields.js";


// It's semi un-documented, but some ticket apis, especially the batch ones,
// let you create a new user inline, for example instead of providing
// requester_id: 234, providing requester: { name: 'name', email: 'example@example.com'}
// this function implements this feature.
function allowInlineNewUser(globalState, obj, keyToUse, keyId) {
    if (obj[keyToUse]) {
        const em = obj[keyToUse].email
        const nm = obj[keyToUse].name
        if (!em || !nm) {
            throw new Error(`attempted inline User but did not pass in an email or name`)
        }
        
        const foundByEmail = usersSearchByEmailImpl(globalState, em)?.users
        if (foundByEmail?.length) {
            const foundByName = foundByEmail.find(user=>user.name === nm)
            if (foundByName) {
                obj[keyId] = normalizeId(foundByName.id)
            } else {
                throw new Error(`attempted inline User but did name does not match existing user with this email`)
            }
        } else {
            const resultUser = transformIncomingUserIntoInternal(globalState, {name: nm, email:em})
            insertPersistedUser(globalState, resultUser)
            console.log(`Created an inline User.`)
            obj[keyId] = resultUser.id
        }
    }

    if (obj[keyId]) {
        obj[keyId] = normalizeId(obj[keyId])
    }
}

export function apiTicketsImportCreateMany(payload) {
    // because this is an 'import' api, we allow setting createdat
    const globalState = getGlobalStateCopy()
    const response = []
    for (let [index, ticket] of payload.tickets.entries()) {
        allowInlineNewUser(globalState, ticket, 'requester', 'requester_id')
        allowInlineNewUser(globalState, ticket, 'submitter', 'submitter_id')
        const resultTicket = transformIncomingTicketImportIntoInternal(globalState, ticket)
        resultTicket.comment_ids = []
        if (ticket.comment) {
            // Zendesk allows this shorthand
            ticket.comments = [ticket.comment]
        }

        for (let [j, comment] of (ticket.comments||[]).entries()) {
            comment = allowShortcutStringComment(comment)
            allowInlineNewUser(globalState, comment, 'author', 'author_id')
            const fallbackAuthorId = j === 0 ? normalizeId(resultTicket.requester_id) : getDefaultAdminId() // Tricky zendesk logic... this seems to match what happens
            const c = transformIncomingCommentIntoInternal(globalState, comment, fallbackAuthorId)
            insertPersistedComment(globalState, c)
            resultTicket.comment_ids.push(c.id)
            // Because this is 'import create many', not 'standard create many', skip triggers
        }

        insertPersistedTicket(globalState, resultTicket)
        response.push({index: index, id: resultTicket.id, account_id: "not yet implemented", "success": true /* extra */})
    }

    // Because this is 'import create many', not 'standard create many', skip triggers
    const newJobId = addJobResultToMemory(globalState, response)
    const finalResponse = renderPendingJob(newJobId)
    saveGlobalState(globalState)
    return finalResponse
}

export function apiTicketUpdateMany(payload) {
    const globalState = getGlobalStateCopy()
    const response = []

    for (let [index, ticket] of payload.tickets.entries()) {
        ticket.id = normalizeId(ticket.id)
        const existing = globalState.persistedState.tickets[ticket.id]
        if (!existing) {
            throw new Error(`cannot update, ticket id ${ticket.id} not found`)
        }

        const resultTicket = transformIncomingTicketUpdateIntoInternal(existing, ticket)
        if (ticket.comments) {
            throw new Error(`you can only set comments when importing`)
        }
        if (ticket.comment) {
            ticket.comment = allowShortcutStringComment(ticket.comment)
            if (ticket.comment.created_at) {
                throw new Error(`you can only set created_at when importing`)
            }

            allowInlineNewUser(globalState, ticket.comment, 'author', 'author_id')
            const c = transformIncomingCommentIntoInternal(globalState, ticket.comment, normalizeId(resultTicket.requester_id))
            insertPersistedComment(globalState, c)
            resultTicket.comment_ids.push(c.id)
            runTriggersOnNewCommentPosted(globalState, resultTicket, c)
        }

        updatePersistedTicket(globalState, resultTicket)
        response.push({index: index, id: resultTicket.id, "action":"update", "status":"Updated", "success":true})
    }

    const newJobId = addJobResultToMemory(globalState, response)
    const finalResponse = renderPendingJob(newJobId)
    saveGlobalState(globalState)
    return finalResponse
}

export function apiTicketsShowMany(payload) {
    const globalState = getGlobalState()
    const ids = payload.split(',')
    const result = []
    for (let id of ids) {
        id = normalizeId(id)
        if (!globalState.persistedState.tickets[id]) {
            console.log(`ticket not found ${id}`)
            continue
        }

        const existing = lodash.cloneDeep(globalState.persistedState.tickets[id])
        existing.fields = [...existing.fields, ...existing.custom_fields]
        result.push(existing)
    }

    result.reverse() // there is no guarenteed ordering
    return {tickets: result}
}


function transformIncomingTicketUpdateIntoInternal(current, incomingUpdate) {
    current = {...current}
    if (current.status == 'closed') {
        throw new Error('cannot update a closed ticket')
    }
    if (incomingUpdate.subject) {
        current.subject = incomingUpdate.subject
    }
    if (incomingUpdate.assignee_email||
        incomingUpdate.group_id||incomingUpdate.organization_id||incomingUpdate.collaborator_ids ||
        incomingUpdate.additional_collaborators||incomingUpdate.followers||incomingUpdate.priority||incomingUpdate.email_ccs) {
        throw new Error("cannot update this property, not yet implemented")
    }

    /* interestingly we can update these */
    if (incomingUpdate.requester_id) {
        current.requester_id = normalizeId(incomingUpdate.requester_id)
    }
    if (incomingUpdate.assignee_id) {
        current.assignee_id = normalizeId(incomingUpdate.assignee_id)
    }

    if (incomingUpdate.status) {
        current.status = incomingUpdate.status
    }
    if (incomingUpdate.additional_tags) { // less documented, but does work on latest api
        assert(Array.isArray(incomingUpdate.additional_tags), 'additional_tags must be an array')
        current.tags = [...incomingUpdate.additional_tags, ...current.tags]
        current.tags = lodash.uniq(current.tags)
    }
    if (incomingUpdate.remove_tags) { // less documented, but does work on latest api
        assert(Array.isArray(incomingUpdate.remove_tags), 'remove_tags must be an array')
        current.tags = current.tags.filter(t=>!incomingUpdate.remove_tags.includes(t))
    }
    if (incomingUpdate.tags) {
        current.tags = incomingUpdate.tags
        current.tags = lodash.uniq(current.tags)
    }
    if (incomingUpdate.external_id||incomingUpdate.problem_id||incomingUpdate.due_at||
        incomingUpdate.updated_stamp||incomingUpdate.sharing_agreement_ids||incomingUpdate.macro_ids ||
        incomingUpdate.attribute_value_ids) {
        throw new Error("cannot update this property, not yet implemented")
    }
    intCustomFields(incomingUpdate.custom_fields)
    if (incomingUpdate.custom_fields) {
        // confirmed in zendesk api that this merges in, not replaces
        // put it in this order so that incoming vals are prioritized
        current.custom_fields = [...incomingUpdate.custom_fields, ...current.custom_fields]
        current.custom_fields = lodash.uniqBy(current.custom_fields, fld=>fld.id)
    }
    
    // ignore safe_update for now, would be good to implement in the future for testing race conditions
    current.updated_at = getCurrentTimestamp()
    return current
}

 // Ticket.CreateModel
function transformIncomingTicketImportIntoInternal(globalState, obj) {
    assert(!obj.id, `new ticket - cannot specify id`)
    if (obj.external_id || obj.type ||  obj.priority || obj.recipient 
        || obj.organization_id || obj.group_id || obj.collaborator_ids || obj.collaborators || 
        obj.follower_ids || obj.email_cc_ids || obj.via_followup_source_id || obj.macro_ids ||
         obj.ticket_form_id || obj.brand_id) {
        throw new Error("cannot set this property, not yet implemented")
    }
    if (obj.fields) {
        throw new Error("cannot set fields, not yet implemented")
    }
    intCustomFields(obj.custom_fields)
    return {
        id: generateTicketId(globalState.persistedState),
        created_at: obj.created_at || getCurrentTimestamp(),
        updated_at: obj.updated_at ||obj.created_at || getCurrentTimestamp(),
        subject: (obj.subject || obj.raw_subject || '(no subject given)'),
        raw_subject: (obj.subject || obj.raw_subject || '(no subject given)'),
        status: obj.status || 'open',
        description: obj.description || '(no description given)',
        requester_id: normalizeId(obj.requester_id || getDefaultAdminId()),
        submitter_id: normalizeId(obj.submitter_id || obj.requester_id || getDefaultAdminId()),
        assignee_id: normalizeId(obj.assignee_id || getDefaultAdminId()),
        tags: obj.tags || [],
        custom_fields: obj.custom_fields || [],
        fields: obj.fields || [],
        is_public: (obj.is_public === undefined) ? true : obj.is_public
    }
}
