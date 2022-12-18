

import fs from 'fs';
import { getCurrentTimestamp } from './api/helpers.js';

/**
 * For simplicity, instead of a db, save state a json file to disk
 * 
 * Reading state:
 * const globalState = getGlobalState()
 * const myVal = globalState.x.y.z
 * 
 * Writing state:
 * First, begin the transaction by getting a copy of state.
 * const globalState = getGlobalStateCopy()
 * Then, make changes,
 * globalState.x.y.z = 'changed'
 * Then, commit the changes both to memory and to disk,
 * saveGlobalState(globalState)
 * If an exception occurs, all changes were made to a copy and so they're intentionally dropped.
 * This way we can guarentee consistency, partial changes will never be saved to disk.
 */
let masterGlobalState = {}

/**
 * Load the file from disk, or create a new empty state if file not found
 */
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
    masterGlobalState['jobResults'] = {}
}


/**
 * Create an empty state
 */
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

/**
 * Get the global state.
 * Used for read operations.
 */
export function getGlobalState() {
    // Prevent callers from making any changes -
    // any changes they accidentally will be dropped and never persisted.
    return getGlobalStateCopy()
}

/**
 * This can be used to mimic transactions,
 * Callers act on a copy, then save the copy when complete.
 * Used for write operations.
 */
export function getGlobalStateCopy() {
    // lodash's clonedeep is another possibility.
    const clone = JSON.parse(JSON.stringify(masterGlobalState))
    return clone
}

/**
 * Commit the changes to disk
 */
export function saveGlobalState(copyGlobalState=undefined) {
    copyGlobalState = copyGlobalState || masterGlobalState
    const s = JSON.stringify(copyGlobalState['persistedState'], null, 1)
    fs.writeFileSync('./persistedGlobalState.json', s, {encoding:'utf-8'})
    masterGlobalState = copyGlobalState
}

/**
 * For simplicity we have one hard-coded admin user.
 * Future feature could be to read credentials in an authentication header
 */
export function getDefaultAdminId() {
    return 111
}

