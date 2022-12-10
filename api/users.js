
import assert from "assert";
import { saveGlobalState, getGlobalStateCopy, getGlobalState } from "../persist.js";
import { addJobResultToMemory, getCurrentTimestamp,  generateUserId, normalizeId } from "./helpers.js";
import { renderPendingJob } from "./jobresults.js";
import { insertPersistedUser, validateInternalUser } from "./schema.js";

export function apiUsersShowMany(payload) {
    const globalState = getGlobalState()
    console.log('**'+payload+'**')
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
    return {users: result}
}

export function apiUsersCreateMany(payload) {
    const globalState = getGlobalStateCopy()
    payload = payload['users']
    const response = []
    for (const [index, userInfo] of payload.entries()) {
        const resultUser = transformIncomingUserIntoInternal(globalState, userInfo)
        const alreadyFound = usersSearchByEmailImpl(globalState, resultUser.email)
        console.log('alreadyfound', JSON.stringify(alreadyFound))
        if (alreadyFound?.users?.length) {
            response.push({"success": true, index: index, id: alreadyFound.users[0].id, "action": "update", "status": "Updated"})
        } else {
            insertPersistedUser(globalState, resultUser)
            response.push({"success": true, index: index, id: resultUser.id, "action": "create", "status": "Created"})
        }
    }

    const newJobId = addJobResultToMemory(globalState, response)
    const finalResponse = renderPendingJob(newJobId)
    saveGlobalState(globalState)
    return finalResponse
}


// /api/v2/users/search?query=email:encodeURIComponent(email)
export function apiUsersSearchByEmail(email) {
    const globalState = getGlobalState()
    return usersSearchByEmailImpl(globalState, email)
}

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


export function transformIncomingUserIntoInternal(globalState, obj) {
    assert(!obj.id, `new user - cannot specify id`)
    return {
        id: generateUserId(globalState.persistedState),
        name: obj.name,
        email: obj.email,
        created_at: getCurrentTimestamp()
    }
}
