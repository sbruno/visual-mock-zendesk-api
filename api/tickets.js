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
