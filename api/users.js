
import assert from "assert";
import { saveGlobalState, getGlobalStateCopy, getGlobalState } from "../persist.js";
import { addJobResultToMemory, getCurrentTimestamp,  generateUserId, normalizeId } from "./helpers.js";
import { renderPendingJob } from "./jobresults.js";
import { insertPersistedUser, validateInternalUser } from "./schema.js";

/**
 * Endpoint for showing user information by id
 */
export function apiUsersShowMany(payload) {
    const globalState = getGlobalState()
    const ids = payload.split(',')
    const result = []
    for (let id of ids) {
        id = normalizeId(id)
        if (!globalState.persistedState.users[id]) {
            // Matching zendesk api, skip and continue
            console.log(`user not found ${id}`)
            continue
        }

        result.push(globalState.persistedState.users[id])
    }
    
    // Reverse the array, to simulate that there is no guarenteed ordering
    result.reverse()
    return {users: result}
}

/**
 * Endpoint for creating users
 */
export function apiUsersCreateMany(payload) {
    const globalState = getGlobalStateCopy()
    assert(payload.users && Array.isArray(payload.users), 'not an array')

    const response = []
    for (const [index, userInfo] of payload.users.entries()) {
        const resultUser = transformIncomingUserIntoInternal(globalState, userInfo)
        const alreadyFound = usersSearchByEmailImpl(globalState, resultUser.email)
        if (alreadyFound?.users?.length) {
            response.push({"success": true, index: index, id: alreadyFound.users[0].id, "action": "update", "status": "Updated"})
        } else {
            // Need to study actual-zendesk to see if this is correct
            insertPersistedUser(globalState, resultUser)
            response.push({"success": true, index: index, id: resultUser.id, "action": "create", "status": "Created"})
        }
    }

    const newJobId = addJobResultToMemory(globalState, response)
    const finalResponse = renderPendingJob(newJobId)
    saveGlobalState(globalState)
    return finalResponse
}


/**
 * Endpoint for searching users by email
 */
export function apiUsersSearchByEmail(email) {
    const globalState = getGlobalState()
    return usersSearchByEmailImpl(globalState, email)
}

/**
 * Internal helper for searching users by email
 */
export function usersSearchByEmailImpl(globalState, email) {
    const allUsers = globalState.persistedState.users
    let results = []
    for (let userId in allUsers) {
        const user = allUsers[userId]
        if (user.email === email) {
            results.push(user)
        }
    }
    return {
        count: results.length,
        users: results
    }
}

/**
 * Validate incoming data
 */
export function transformIncomingUserIntoInternal(globalState, obj) {
    assert(!obj.id, `new user - cannot specify id`)
    return {
        id: generateUserId(globalState.persistedState),
        name: obj.name,
        email: obj.email,
        created_at: getCurrentTimestamp()
    }
}
