
import assert from "assert";
import { saveGlobalState, getGlobalStateCopy, getGlobalState } from "../persist.js";
import { addJobResultToMemory, getCurrentTimestamp,  generateUserId } from "./helpers.js";
import { renderPendingJob } from "./jobresults.js";
import { validateInternalUser } from "./schema.js";

export function apiUsersShowMany(payload) {
    const globalState = getGlobalState()
    const ids = payload.split(',')
    const result = []
    for (let id of ids) {
        id = id.trim()
        if (!parseInt(id)) {
            throw new Error(`not a user id ${id}`)
        }
        if (!globalState.persistedState.users[id]) {
            throw new Error(`user not found ${id}`)
        }
        result.push(globalState.persistedState.users[id])
    }
    return {users: result}
}

export function apiUsersCreateMany(payload) {
    const globalState = getGlobalStateCopy()
    payload = payload['users']
    const result = []
    for (const [index, userInfo] of payload.entries()) {
        userInfo = validateIncomingUserParams(userInfo)
        emailCannotExistTwice(globalState, userInfo.email) 

        newId = createUser(userInfo.name, userInfo.email)
        result.push({index: index, id: newId})
    }

    const newJobId = addJobResultToMemory(globalState, result)
    saveGlobalState(globalState)
    return renderPendingJob(newJobId)
}

export function createUser(globalState, name, email) {
    const newId = generateUserId(globalState.persistedState)
    const newUser = validateInternalUser({
        id: newId,
        name,
        email,
        created_at: getCurrentTimestamp(),
    })
    globalState.persistedState.users[newId] = newUser

    return newId
}

function emailCannotExistTwice(globalState, email) {
    const allUsers = globalState.persistedState.users
    for (let userId in allUsers) {
        const user = allUsers[userId]
        if (user.email === email) {
            assert(false, 'user with this email already exists ' + email)
        }
    }
}

// /api/v2/users/search?query=email:encodeURIComponent(email)
export function apiUsersSearchByEmail(email) {
    const globalState = getGlobalState()
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

