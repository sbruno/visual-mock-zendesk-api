import { getGlobalState } from "../persist.js"
import lodash from 'lodash'
import { normalizeId } from "./helpers.js"

/**
 * Show the values for custom fields in a user-friendly way.
 * If an unknown id is provided, we'll just show the id number.
 */
export function renderCustomFields(ticket) {
    if (!ticket.custom_fields) {
        return ''
    }
    
    const globalState = getGlobalState()
    const customFldMap = globalState?.globalConfigs?.customFields
    const mapIdToName = customFldMap ? lodash.invert(customFldMap) : {}
    const arr = (ticket.custom_fields || []).map(fld=>{
        const name = mapIdToName[fld.id] || fld.id
        const val = fld.value
        return `${name} = ${val}`
    })
    
    return arr.join('\n')
}

/**
 * Custom fields are in an array, so this helper makes it easier to retrieve a value.
 */
export function getCustomFldVal(ticket, id) {
    if (!ticket?.custom_fields) {
        return undefined
    }

    for (let fld of ticket.custom_fields) {
        if (parseInt(fld.id) === id) {
            return fld.value
        }
    }

    return undefined
}

/**
 * More id normalization, to correctly accept string ids from the user.
 */
export function intCustomFields(custom_fields) {
    if (custom_fields) {
        for (let fld of custom_fields) {
            if (fld.id) {
                fld.id = normalizeId(fld.id)
            }
        }
    }
}
