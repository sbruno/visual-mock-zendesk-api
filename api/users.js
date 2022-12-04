
import assert from "assert";
import { saveGlobalState, getGlobalStateCopy, getGlobalState } from "../persist.js";
import { addJobResultToMemory, getCurrentTime } from "./helpers.js";

export function createManyUsers(payload) {
    const globalState = getGlobalStateCopy()
    payload = payload['users']
    const result = []
    for (let userInfo of payload) {
        assert(userInfo.name, 'must have a name')
        assert(userInfo.email, 'must have a email')
        emailCannotExistTwice(globalState, userInfo.email) 
        const newId = generateUserId()
        const newUser = {
            id: newId,
            name: userInfo.name,
            email: userInfo.email,
            created_at: getCurrentTime(),
        }
        globalState.persistedState.users[newId] = newUser
        result.push({id: newId})
    }

    const fullResult = {
        job_status: {status: 'completed', results: result},
    }
    addJobResultToMemory(globalState, fullResult)
    saveGlobalState(globalState)
}

function emailCannotExistTwice(globalState, email) {
    const allUsers = globalState.persistedState.users
    for (let user of allUsers) {
        if (user.email === email) {
            assert(false, 'user with this email already exists ' + email)
        }
    }
}

// /api/v2/users/search?query=email:encodeURIComponent(email)
export function searchByEmail(email) {
    console.log('looking for email|' + email + '|')
    const globalState = getGlobalState()
    const allUsers = globalState.persistedState.users
    let results = []
    for (let user of allUsers) {
        if (user.email === email) {
            results.push(user)
        }
    }
    return {
        count: results.length,
        users: results
    }
}

