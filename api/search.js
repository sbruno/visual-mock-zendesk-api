import { errNotImplemented } from "./apiroutes.js"
import lodash from 'lodash'
import { getGlobalState } from "../persist.js"
import { normalizeId } from "./helpers.js"
import { getCustomFldVal } from "./customfields.js"

class BaseFilter {
    includeThese = []
    excludeThese = []
    getFilter() {
        throw new Error('implement in child class')
    }
}

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
                return t.tags.any(tag => this.includeThese.includes(tag))
            }
        } else if (this.excludeThese.length) {
            return (t)=>{
                if (!t?.tags?.length) {
                    return true
                }
                return !t.tags.any(tag => this.excludeThese.includes(tag))
            }
        } else {
            return (t)=>true
        }
    }
}

class FilterCustomField extends BaseFilter {
    constructor(id) {
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

export function apiSearch(query, sortBy, sortOrder) {
    const globalState = getGlobalState()
    sortBy = sortBy || 'created_at'
    sortOrder = sortOrder || 'asc'
    const queryParts = query.split(' ')
    const filters = {}
    filters.filterStatus = new FilterStatus()
    filters.filterTag = new FilterByTag()
    const addCustomFieldFilter = (s, isExclude) => {
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
            filterStatus.includeThese.push(s)
        } else if (part.startsWith('-status:')) {
            const s = part.slice('-status:'.length)
            filterStatus.excludeThese.push(s)
        } else if (part.startsWith('tags:')) {
            const s = part.slice('tags:'.length)
            filterTag.includeThese.push(s)
        } else if (part.startsWith('-tags:')) {
            const s = part.slice('-tags:'.length)
            filterTag.excludeThese.push(s)
        } else if (part.startsWith('custom_field_')) {
            const s = part.slice('custom_field_'.length)
            addCustomFieldFilter(s, false)
        } else if (part.startsWith('-custom_field_')) {
            const s = part.slice('-custom_field_'.length)
            addCustomFieldFilter(s, true)
        } 
    }

    let results = Object.values(globalState.persistedState.tickets)
    results = results.filter(t=> {
        for (let filter of Object.values(filters)) {
           const filterFn = filter.getFilter()
           if (!filterFn(t)) {
            return false
           }
        }
        return true
    })

    results = lodash.sortBy(results, sortBy)
    if (sortOrder == 'desc') {
        results.reverse()
    }

    return {
        count: results.length,
        results: results
    }
}

