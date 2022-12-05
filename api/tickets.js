import { getCurrentTimestamp } from "./helpers.js"
import { validateInternalTicket } from "./schema.js"
import lodash from 'lodash'
import { saveGlobalState } from "../persist.js"
import { renderPendingJob } from "./jobresults.js"

// '/api/v2/imports/tickets/create_many'
export function apiImportCreateMany(payload) {
    // because this is an 'import' api, we allow setting createdat
    const globalState = getGlobalStateCopy()
    for (let ticket of payload.tickets) {
        const obj = createTicket(globalState, ticket.subject, ticket.status, ticket.custom_fields, ticket.is_public, ticket.requester_id, ticket.submitter_id, ticket.tags, ticket.created_at)
        if (ticket.comments) {
            for (let comment of ticket.comments) {

            }
        }
    }
    saveGlobalState(globalState)
    return renderPendingJob(newJobId)
}

export function apiUpdateTicket(payload) {
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

export function createTicket(globalState, created_at, subject, status, custom_fields, is_public,
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
