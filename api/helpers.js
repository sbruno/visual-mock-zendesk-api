

import assert from "assert";
import crypto from 'crypto';

export const portNumber = 8999

export function generateUserId(persistedState) {
    assert(persistedState['users'])
    for (let i=0; i<5; i++) {
        let candidate = genCandidate()
        if (!persistedState['users'][candidate]) {
            return candidate
        }
    }

    assert(false, 'could not generate user id')
}

export function generateTicketId(persistedState) {
    assert(persistedState['tickets'])
    for (let i=0; i<5; i++) {
        let candidate = genCandidate()
        if (!persistedState['tickets'][candidate]) {
            return candidate
        }
    }

    assert(false, 'could not generate ticket id')
}

export function generateCommentId(persistedState) {
    assert(persistedState['comments'])
    for (let i=0; i<5; i++) {
        let candidate = genCandidate()
        if (!persistedState['comments'][candidate]) {
            return candidate
        }
    }

    assert(false, 'could not generate comment id')
}

export function addJobResultToMemory(globalState, payload) {
    const jobId = crypto.randomUUID()
    if (!globalState['jobresults']) {
        globalState['jobresults'] = {}
    }
    
    globalState['jobresults'][jobId] = payload
    return jobId
}

export function getCurrentTimestamp() {
    // 2020-04-09T20:37:31.451Z
    // 2022-11-27T22:12:23.546Z
    const dt = new Date()
    return dt.toISOString()
}

export function validateJustTheseKeys() {

}

function genCandidate() {
    return Math.round(Math.random() * 1000 * 1000)
}