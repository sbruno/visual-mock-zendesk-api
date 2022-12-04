

import fs from 'fs';

let globalState = {}

function onLoad() {
    globalState = {}
    if (!fs.existsSync('./persistedGlobalState.json')) {
        resetPersistedState()
    }
    
    const contents = fs.readFileSync('./persistedGlobalState.json', {encoding:'utf-8'})
    globalState['persistedState'] = JSON.parse(contents)
}

onLoad()

export function resetPersistedState() {
    const empty = {
        users: {'111': {
            id: '111',
            created_at: '123',
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

export function saveGlobalState() {
    const s = JSON.stringify(globalState['persistedState'])
    fs.writeFileSync('./persistedGlobalState.json', s, {encoding:'utf-8'})
}
