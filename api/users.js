
import assert from "assert";
import { saveGlobalState, getGlobalStateCopy, getGlobalState } from "../persist.js";
import { addJobResultToMemory, getCurrentTimestamp } from "./helpers.js";
import { validateInternalUser } from "./schema.js";

export function usersCreateMany(payload) {
    const globalState = getGlobalStateCopy()
    payload = payload['users']
    const result = []
    for (const [index, userInfo] of payload.entries()) {
        assert(userInfo.name, 'must have a name')
        assert(userInfo.email, 'must have a email')
        emailCannotExistTwice(globalState, userInfo.email) 
        const newId = generateUserId()
        const newUser = validateInternalUser({
            id: newId,
            name: userInfo.name,
            email: userInfo.email,
            created_at: getCurrentTimestamp(),
        })

        globalState.persistedState.users[newId] = newUser
        result.push({index: index, id: newId})
    }

    const newJobId = addJobResultToMemory(globalState, result)
    saveGlobalState(globalState)
    return renderPendingJob(newJobId)
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
export function searchByEmail(email) {
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

