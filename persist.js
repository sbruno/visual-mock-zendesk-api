

import fs from 'fs';
import { getCurrentTimestamp } from './api/helpers.js';

let globalState = {}

export function onLoad() {
    globalState = {}
    if (!fs.existsSync('./persistedGlobalState.json')) {
        resetPersistedState()
    }

    if (fs.existsSync('./configs.json')) {
        const contentConfigs = fs.readFileSync('./configs.json', {encoding:'utf-8'})
        globalState['globalConfigs'] = JSON.parse(contentConfigs)
    } else {
       throw new Error('No configs.json was found. Create one with the contents {} if needed.')
    }
    
    const contents = fs.readFileSync('./persistedGlobalState.json', {encoding:'utf-8'})
    globalState['persistedState'] = JSON.parse(contents)
}

export function getDefaultAdminId() {
    return 111
}
export function resetPersistedState() {
    const empty = {
        users: {[getDefaultAdminId()]: {
            id: getDefaultAdminId(),
            created_at: getCurrentTimestamp(),
            email: 'zendeskmockadmin@zendeskmockadmin.com',
            name: 'ZendeskMockAdmin',
        }},
        tickets: {},
        comments: {},
    }
    const s = JSON.stringify(empty, null, 1)
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
    const s = JSON.stringify(copyGlobalState['persistedState'], null, 1)
    fs.writeFileSync('./persistedGlobalState.json', s, {encoding:'utf-8'})
    globalState = copyGlobalState
}
