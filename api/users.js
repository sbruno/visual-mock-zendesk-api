
import assert from "assert";
import { addJobResultToMemory, getCurrentTime } from "./helpers";

export function create_many_users(globalState, payload) {
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
}

function emailCannotExistTwice(globalState, email) {
    const allUsers = globalState.persistedState.users
    for (let user of allUsers) {
        if (user.email === email) {
            assert(false, 'user with this email already exists ' + email)
        }
    }
}

