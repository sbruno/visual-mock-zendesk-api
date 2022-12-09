import { getGlobalState } from "../persist.js"
import lodash from 'lodash'


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
