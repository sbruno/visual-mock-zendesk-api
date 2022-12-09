
import assert from "assert";
import { saveGlobalState, getGlobalStateCopy, getGlobalState } from "../persist.js";
import { addJobResultToMemory, getCurrentTimestamp,  generateUserId } from "./helpers.js";
import { renderPendingJob } from "./jobresults.js";
import { insertPersistedUser, validateInternalUser } from "./schema.js";

export function apiUsersShowMany(payload) {
    const globalState = getGlobalState()
    const ids = payload.split(',')
    const result = []
    for (let id of ids) {
        id = id.trim()
        if (!parseInt(id)) {
            throw new Error(`not a user id ${id}`)
        } else if (!globalState.persistedState.users[id]) {
            throw new Error(`user not found ${id}`)
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
        if (alreadyFound && alreadyFound?.results?.length) {
            response.push({"success": true, index: index, id: alreadyFound.results[0].id, "action": "update", "status": "Updated"})
        } else {
            insertPersistedUser(globalState, resultUser)
            response.push({"success": true, index: index, id: resultUser.id, "action": "create", "status": "Created"})
        }
    }

    const newJobId = addJobResultToMemory(globalState, response)
    saveGlobalState(globalState)
    return renderPendingJob(newJobId)
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
