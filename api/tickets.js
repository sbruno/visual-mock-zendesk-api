import { getCurrentTimestamp } from "./helpers.js"
import { validateInternalTicket } from "./schema.js"
import lodash from 'lodash'
import { saveGlobalState } from "../persist.js"
import { renderPendingJob } from "./jobresults.js"
import { apiUsersSearchByEmail, createUser } from "./users.js"



function allowInlineNewUser(globalState, obj, keyToUse, keyId) {
    if (obj[keyToUse]) {
        const em = obj[keyToUse].email
        const nm = obj[keyToUse].name
        if (!em || !nm) {
            throw new Error(`attempted inline User but did not pass in an email or name`)
        }
        const foundByEmail = apiUsersSearchByEmail(em)?.users
        if (foundByEmail) {
            const foundByName = foundByEmail.find(user.name === nm)
            if (foundByName) {
                obj[keyId] = foundByName.id
            } else {
                throw new Error(`attempted inline User but did name does not match existing user with this email`)
            }
        } else {
            const newId = createUser(globalState, nm, em)
            console.log(`created inline User`)
            obj[keyId] = newId
        }
    }
}

export function apiTicketsImportCreateMany(payload) {
    // because this is an 'import' api, we allow setting createdat
    const globalState = getGlobalStateCopy()
    for (let ticket of payload.tickets) {
        allowInlineNewUser(globalState, ticket, 'requester', 'requester_id')
        allowInlineNewUser(globalState, ticket, 'submitter', 'submitter_id')
        const obj = ticketCreate(globalState, ticket.subject, ticket.status, ticket.custom_fields, ticket.is_public, ticket.requester_id, ticket.submitter_id, ticket.tags, ticket.created_at)
        if (ticket.comments) {
            for (let comment of ticket.comments) {
                allowInlineNewUser(globalState, comment, 'author', 'author_id')
                const c = commentCreate()

            }
        }
    }

    saveGlobalState(globalState)
    return renderPendingJob(newJobId)
}

export function apiTicketUpdate(payload) {
    const globalState = getGlobalStateCopy()
    saveGlobalState(globalState)
    return renderPendingJob(newJobId)
}

export function updateTicket(globalState, id, status, custom_fields, is_public, tags) {
    const existingTicket = globalState.persistedState.tickets[id]
    if (!existingTicket) {
        throw new Error(`no existing ticket with id ${id}`)
    }
    ticket.modified_at = getCurrentTimestamp()
    ticket.status = status || ticket.status
    applyCustomFields(ticket, custom_fields)
    ticket.is_public = is_public
    ticket.tags = [...ticket.tags, ...tags]
    ticket.tags = lodash.uniq(ticket.tags)
    validateInternalTicket(ticket)
    runTriggersOnNewCommentPosted
}

function applyCustomFields(ticket, custom_fields) {
    if (!custom_fields || !custom_fields.length) {
        return
    }
    //merge it
}

export function ticketCreate(globalState, created_at, subject, status, custom_fields, is_public,
     requester_id, submitter_id, tags) {
    submitter_id = submitter_id || requester_id
    
    const result = {
        id: generateTicketId(globalState.persistedState),
        created_at: createdAt || getCurrentTimestamp(),
        subject: subject,
        raw_subject: subject,
        status: status || 'open',
        requester_id: requester_id,
        submitter_id: submitter_id,
        tags: tags || [],
        is_public: is_public || true,
        custom_fields: custom_fields || [],
        fields: [],
        comment_ids: []
    }

    assert(globalState.persistedState.users[requester_id], 'requester_id id not found:' + requester_id)
    assert(globalState.persistedState.users[submitter_id], 'submitter_id id not found:' + submitter_id)
    result.modified_at = result.created_at
    return result
}

export function addTicket(globalState, obj) {
    obj = validateInternalTicket(obj)
    globalState.persistedState.tickets[obj.id] = obj
}

export function apiShowManyTickets(payload) {
    const globalState = getGlobalState()
    const ids = payload.split(',')
    const result = []
    for (let id of ids) {
        id = id.trim()
        if (!parseInt(id)) {
            throw new Error(`not a ticket id ${id}`)
        }
        if (!globalState.persistedState.tickets[id]) {
            throw new Error(`ticket not found ${id}`)
        }
        result.push(globalState.persistedState.tickets[id])
    }
    return {tickets: result}
}


function transformIncomingTicketUpdateIntoInternal(existing, incomingUpdate) {
    if (existing.status == 'closed') {
        throw new Error('cannot update a closed ticket')
    }
    if (incomingUpdate.subject) {
        existing.subject = incomingUpdate.subject
    }
    if (incomingUpdate.requester_id||incomingUpdate.assignee_id||incomingUpdate.assignee_email||
        incomingUpdate.group_id||incomingUpdate.organization_id||incomingUpdate.collaborator_ids ||
        incomingUpdate.additional_collaborators||incomingUpdate.followers||incomingUpdate.priority||incomingUpdate.email_ccs) {
        throw new Error("cannot update this property, not yet implemented")
    }
    if (incomingUpdate.status) {
        existing.status = incomingUpdate.status
    }
    if (incomingUpdate.additional_tags) { // less documented, but does work on latest api
        assert(Array.isArray(incomingUpdate.additional_tags), 'additional_tags must be an array')
        existing.tags = [...existing.tags, ...incomingUpdate.additional_tags]
        existing.tags = lodash.uniq(existing.tags)
    }
    if (incomingUpdate.remove_tags) { // less documented, but does work on latest api
        assert(Array.isArray(incomingUpdate.remove_tags), 'remove_tags must be an array')
        existing.tags = existing.tags.filter(t=>!incomingUpdate.remove_tags.includes(t))
    }
    if (incomingUpdate.tags) {
        existing.status = incomingUpdate.tags
    }
    if (incomingUpdate.external_id||incomingUpdate.problem_id||incomingUpdate.due_at||
        incomingUpdate.updated_stamp||incomingUpdate.sharing_agreement_ids||incomingUpdate.macro_ids ||
        incomingUpdate.attribute_value_ids) {
        throw new Error("cannot update this property, not yet implemented")
    }
    if (incomingUpdate.custom_fields) {
        // confirmed in zendesk api that this merges in, not replaces
        existing.custom_fields = {...existing.custom_fields, ...incomingUpdate.custom_fields}
    }
    
    // ignore safe_update for now, would be good to implement in the future for testing race conditions
    existing.modified_at = getCurrentTimestamp()
}

function transformIncomingTicketImportIntoInternal(obj) { // CreateModel
    assert(!obj.id, `new ticket - cannot specify id`)
    // we've used requester->requesterid
    if (obj.external_id || obj.type ||  obj.priority || obj.recipient 
        || obj.organization_id || obj.group_id || obj.collaborator_ids || obj.collaborators || 
        obj.follower_ids || obj.email_cc_ids || obj.xxxx || obj.xxxx || obj.xxxx || obj.xxxx ||) {
        throw new Error("cannot update this property, not yet implemented")
    }
    return {
        subject: (obj.subject || obj.raw_subject || '(no subject given)'),
        raw_subject: (obj.subject || obj.raw_subject || '(no subject given)'),
        status: (obj.status),
        requester_id: obj.requester_id,
        submitter_id: obj.submitter_id || obj.requester_id,
        assignee_id: obj.assignee_id || getDefaultAdminId(),
        tags: obj.tags || [],
    }
    
}