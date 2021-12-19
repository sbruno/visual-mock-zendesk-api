

import assert from "assert";
import { getGlobalState } from "../persist.js";

/**
 * Port number that we're running on
 */
export function getPortNumber() {
    const globalState = getGlobalState()
    return globalState.globalConfigs?.portNumber || 8999
}

/**
 * Generate a user id, randomly chosen integer
 */
export function generateUserId(persistedState) {
    assert(persistedState['users'])
    for (let i = 0; i < 5; i++) {
        let candidate = genCandidate()
        if (!persistedState['users'][candidate]) {
            return candidate
        }
    }

    assert(false, 'could not generate user id')
}

/**
 * Generate a comment id, randomly chosen integer
 */
export function generateCommentId(persistedState) {
    assert(persistedState['comments'])
    for (let i = 0; i < 5; i++) {
        let candidate = genCandidate()
        if (!persistedState['comments'][candidate]) {
            return candidate
        }
    }

    assert(false, 'could not generate comment id')
}

/**
 * Generate a ticket id, randomly chosen integer
 * In actual zendesk these are always increasing
 */
export function generateTicketId(persistedState) {
    assert(persistedState['tickets'])
    for (let i = 0; i < 5; i++) {
        let candidate = genCandidate()
        if (!persistedState['tickets'][candidate]) {
            return candidate
        }
    }

    assert(false, 'could not generate ticket id')
}

/**
 * Generate a status id, randomly chosen integer
 * In actual zendesk these can be alphanumeric
 */
export function generateJobId(globalState) {
    assert(globalState['jobResults'])
    for (let i = 0; i < 5; i++) {
        let candidate = genCandidate()
        if (!globalState['jobResults'][candidate]) {
            return candidate
        }
    }

    assert(false, 'could not generate job id')
}

/**
 * Accept it if users pass in IDs as a string...
 * Handle it if they pass in `id:"123"`
 */
export function normalizeId(id) {
    const ret = parseInt(id)
    if (!Number.isFinite(ret)) {
        throw new Error('could not parse id, ' + id)
    }

    return ret
}

/**
 * Call normalizeId if present
 */
export function normalizeIdIfPresent(obj, keyId) {
    if (obj[keyId]) {
        obj[keyId] = normalizeId(obj[keyId])
    }
}

/**
 * Store a job in memory. Ephemeral, will be lost on app restart/app exit.
 */
export function addJobResultToMemory(globalState, payload) {
    const jobId = generateJobId(globalState)
    globalState['jobResults'][jobId] = payload
    return jobId
}

/**
 * Gets the current time in iso format
 */
export function getCurrentTimestamp() {
    // Like this, 2020-04-09T20:37:31.451Z
    const dt = new Date()
    return dt.toISOString()
}


/**
 * Helper to indicate what isn't yet impemented
 */
export function errNotImplemented(s) {
    return new Error(`not implemented: ${s}`)
}

/**
 * Generate random integer
 */
function genCandidate() {
    return Math.round(Math.random() * 1000 * 1000)
}
