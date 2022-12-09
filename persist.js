

import fs from 'fs';
import { getCurrentTimestamp } from './api/helpers.js';

let masterGlobalState = {}

export function onLoad() {
    masterGlobalState = {}
    if (!fs.existsSync('./persistedGlobalState.json')) {
        resetPersistedState()
    }

    if (fs.existsSync('./configs.json')) {
        const contentConfigs = fs.readFileSync('./configs.json', {encoding:'utf-8'})
        masterGlobalState['globalConfigs'] = JSON.parse(contentConfigs)
    } else {
       throw new Error('No configs.json was found. Create one with the contents {} if needed.')
    }
    
    const contents = fs.readFileSync('./persistedGlobalState.json', {encoding:'utf-8'})
    masterGlobalState['persistedState'] = JSON.parse(contents)
}

export function getDefaultAdminId() {
    return 111
}

export function resetPersistedState() {
    const empty = {
        users: {
            [getDefaultAdminId()]: {
                id: getDefaultAdminId(),
                created_at: getCurrentTimestamp(),
                email: 'zendeskmockadmin@zendeskmockadmin.com',
                name: 'ZendeskMockAdmin',
            }
        },
        tickets: {},
        comments: {},
    }
    
    const s = JSON.stringify(empty, null, 1)
    fs.writeFileSync('./persistedGlobalState.json', s, {encoding:'utf-8'})
}

export function getGlobalState() {
    // We trust that callers won't make any changes.
    // For a larger project, we'd prevent this, for example only exposing getters.
    return masterGlobalState
}

export function getGlobalStateCopy() {
    // This can be used to mimic transactions,
    // Callers act on a copy, then save the copy when complete.
    const clone = JSON.parse(JSON.stringify(masterGlobalState))
    return clone
}

export function saveGlobalState(copyGlobalState=undefined) {
    copyGlobalState = copyGlobalState || masterGlobalState
    const s = JSON.stringify(copyGlobalState['persistedState'], null, 1)
    fs.writeFileSync('./persistedGlobalState.json', s, {encoding:'utf-8'})
    masterGlobalState = copyGlobalState
}
