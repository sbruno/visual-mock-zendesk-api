import { getGlobalState } from "../persist.js"
import lodash from 'lodash'


export function renderCustomFields(ticket) {
    const globalState = getGlobalState()
    const customFldMap = globalState?.globalConfigs?.customFields
    const mapIdToName = customFldMap ? lodash.invert(customFldMap) : {}
    const arr = (ticket.custom_fields || []).map(fld=>{
        const name = mapIdToName[fld.id] || fld.id
        const val = fld.value
        return `Field ${name} = ${value}`
    })
    
    return arr.join('\n')
}
