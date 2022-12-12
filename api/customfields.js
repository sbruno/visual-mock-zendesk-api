import { getGlobalState } from "../persist.js"
import lodash from 'lodash'
import { normalizeId } from "./helpers.js"


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

export function intCustomFields(custom_fields) {
    if (custom_fields) {
        for (let fld of custom_fields) {
            if (fld.id) {
                fld.id = normalizeId(fld.id)
            }
        }
    }
}
