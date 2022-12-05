

import fs from 'fs';
import { getCurrentTimestamp } from './api/helpers.js';

let globalState = {}

export function onLoad() {
    globalState = {}
    if (!fs.existsSync('./persistedGlobalState.json')) {
        resetPersistedState()
    }
    
    const contents = fs.readFileSync('./persistedGlobalState.json', {encoding:'utf-8'})
    globalState['persistedState'] = JSON.parse(contents)
}


export function resetPersistedState() {
    const empty = {
        users: {'111': {
            id: '111',
            created_at: getCurrentTimestamp(),
            email: 'zendeskmockadmin@zendeskmockadmin.com',
            name: 'ZendeskMockAdmin',
        }},
        tickets: {},
        comments: {},
    }
    const s = JSON.stringify(empty)
    fs.writeFileSync('./persistedGlobalState.json', s, {encoding:'utf-8'})
}

export function getGlobalState() {
    return globalState
}

export function getGlobalStateCopy() {
    const clone = JSON.parse(JSON.stringify(globalState))
    return clone
}

export function saveGlobalState(copyGlobalState=undefined) {
    copyGlobalState = copyGlobalState || globalState
    const s = JSON.stringify(copyGlobalState['persistedState'])
    fs.writeFileSync('./persistedGlobalState.json', s, {encoding:'utf-8'})
    globalState = copyGlobalState
}
