import { errNotImplemented } from "./apiroutes.js"
import lodash from 'lodash'
import { getGlobalState } from "../persist.js"
import { normalizeId } from "./helpers.js"
import { getCustomFldVal } from "./customfields.js"

/**
 * xxx
 */
class BaseFilter {
    includeThese = []
    excludeThese = []
    getFilter() {
        throw new Error('implement in child class')
    }
}

/**
 * xxx
 */
class FilterStatus extends BaseFilter {
    getFilter() {
        if (this.includeThese.length && this.excludeThese.length) {
            throw errNotImplemented(`FilterStatus cannot have both include and exclude`)
        }

        if (this.includeThese.length) {
            return (t)=>this.includeThese.includes(t.status)
        } else if (this.excludeThese.length) {
            return (t)=>!this.excludeThese.includes(t.status)
        } else {
            return (t)=>true
        }
    }
}

/**
 * xxx
 */
class FilterByTag extends BaseFilter {
    getFilter() {
        if (this.includeThese.length && this.excludeThese.length) {
            throw errNotImplemented(`FilterByTag cannot have both include and exclude`)
        }

        if (this.includeThese.length) {
            return (t)=>{
                if (!t?.tags?.length) {
                    return false
                }
                return t.tags.some(tag => this.includeThese.includes(tag))
            }
        } else if (this.excludeThese.length) {
            return (t)=>{
                if (!t?.tags?.length) {
                    return true
                }
                return !t.tags.some(tag => this.excludeThese.includes(tag))
            }
        } else {
            return (t)=>true
        }
    }
}

/**
 * xxx
 */
class FilterCustomField extends BaseFilter {
    constructor(id) {
        super()
        this.id = normalizeId(id)
    }
    getFilter() {
        if (this.includeThese.length && this.excludeThese.length) {
            throw errNotImplemented(`FilterCustomField ${this.id} cannot have both include and exclude`)
        }

        if (this.includeThese.length) {
            return (t)=>{
                const v = getCustomFldVal(t, this.id)
                return this.includeThese.includes(v)
            }
        } else if (this.excludeThese.length) {
            return (t)=>{
                const v = getCustomFldVal(t, this.id)
                return !this.excludeThese.includes(v)
            }
        } else {
            return (t)=>true
        }
    }
}

/**
 * xxx
 */
export function apiSearch(query, sortBy, sortOrder) {
    const globalState = getGlobalState()
    sortBy = sortBy || 'created_at'
    sortOrder = sortOrder || 'asc'
    if (query.includes('%20')) {
        throw new Error('still escaped?', query)
    }
    const queryParts = query.split(' ')
    const filters = {}
    filters.filterStatus = new FilterStatus()
    filters.filterTag = new FilterByTag()
    const addCustomFieldFilter = (s, isExclude) => {
        if (!s.includes(':')) {
            throw new Error('Expected custom_id_12345:abc, got ' + s)
        }

        const id = s.split(':')[0]
        const val = s.split(':')[1]
        if (!filters[id]) {
            filters[id] = new FilterCustomField(id)
        }
        if (isExclude) {
            filters[id].excludeThese.push(val)
        } else {
            filters[id].includeThese.push(val)
        }
    }
    
    for (let part of queryParts) {
        part = part.trim()
        if (!part) {
            continue
        } else if (part.startsWith('updated')) {
            console.log('updated clause is currently ignored.')
        } else if (part.startsWith('status:')) {
            const s = part.slice('status:'.length)
            filters.filterStatus.includeThese.push(s)
        } else if (part.startsWith('-status:')) {
            const s = part.slice('-status:'.length)
            filters.filterStatus.excludeThese.push(s)
        } else if (part.startsWith('tags:')) {
            const s = part.slice('tags:'.length)
            filters.filterTag.includeThese.push(s)
        } else if (part.startsWith('-tags:')) {
            const s = part.slice('-tags:'.length)
            filters.filterTag.excludeThese.push(s)
        } else if (part.startsWith('custom_field_')) {
            const s = part.slice('custom_field_'.length)
            addCustomFieldFilter(s, false)
        } else if (part.startsWith('-custom_field_')) {
            const s = part.slice('-custom_field_'.length)
            addCustomFieldFilter(s, true)
        } 
    }

    let results = Object.values(globalState.persistedState.tickets)
    results = lodash.sortBy(results, 'created_at')
    results = results.filter(t=> {
        for (let key of Object.keys(filters)) {
            let filter = filters[key]
           const filterFn = filter.getFilter()
           if (!filterFn(t)) {
            return false
           }
        }

        return true
    })

    results = lodash.sortBy(results, sortBy)
    if (sortOrder === 'desc') {
        results.reverse()
    }

    return {
        count: results.length,
        results: results
    }
}

