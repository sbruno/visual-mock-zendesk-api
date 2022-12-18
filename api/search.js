
import lodash from 'lodash'
import { getGlobalState } from "../persist.js"
import { errNotImplemented, normalizeId } from "./helpers.js"
import { getCustomFldVal } from "./customfields.js"

/**
 * Base class for search filters
 * 
 * The way Zendesk's search api works is this:
 * if you specify "tags:a tags:b" this means to search for
 * tags:a OR tags:b
 * (tickets with a, tickets with b, and tickets with both are included)
 * 
 * and you can say "-tags:a" to exclude tickets with the a tag.
 * 
 * We don't currently support something like tags:a -tags:b
 */
class BaseFilter {
    includeThese = []
    excludeThese = []
    getFilter() {
        throw new Error('implement in child class')
    }
}

/**
 * Filter by ticket status
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
 * Filter by tag
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
 * Filter by custom id.
 * We'll have separate instances of this class for each custom id, since they are independent,
 * e.g. if the user searches custom_field_1234:abc custom_field_5678:def they work separately
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
                const vOrUndefined = getCustomFldVal(t, this.id)
                return this.includeThese.includes(vOrUndefined)
            }
        } else if (this.excludeThese.length) {
            return (t)=>{
                const vOrUndefined = getCustomFldVal(t, this.id)
                return !this.excludeThese.includes(vOrUndefined)
            }
        } else {
            return (t)=>true
        }
    }
}

/**
 * Endpoint for searching
 */
export function apiSearch(query, sortBy, sortOrder) {
    const globalState = getGlobalState()
    sortBy = sortBy || 'created_at'
    sortOrder = sortOrder || 'asc'
    if (query.includes('%20')) {
        throw new Error('still escaped?', query)
    }

    // filters will have keys like 'filterStatus' and '123' where 123 is a customfld id
    const filters = {}
    filters.filterStatus = new FilterStatus()
    filters.filterTag = new FilterByTag()
    const addCustomFieldFilter = (s, isExclude) => {
        // we've already stripped 'custom_field_' prefix, so s looks like '12345:abc
        if (!s.includes(':')) {
            throw new Error('Expected custom_field_12345:abc, got ' + s)
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
    
    const queryParts = query.split(' ')
    for (let part of queryParts) {
        part = part.trim()
        if (!part) {
            continue
        } else if (part.startsWith('updated')) {
            console.log('updated clause is currently ignored.')
        } else if (part.startsWith('type')) {
            console.log('type clause is currently ignored (assumed to be ticket).')
        }else if (part.startsWith('sort')) {
            console.log('sort clause is currently ignored (use sort_by query param).')
        }else if (part.startsWith('order_by')) {
            console.log('order_by clause is currently ignored (use sort_order query param).')
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

    if (sortBy === 'created_at' || sortBy === 'updated_at') {
        // lexical sort might have been ok, if we knew everything was exactly the same iso8601 format, but that
        // is too much of an assumption. in the future better to store this internally as int milliseconds
        results = lodash.sortBy(results, t=> {
            const dtString = t[sortBy]
            const d = new Date(dtString)
            // get milliseconds since epoch
            return d.valueOf()
        })
    } else {
        results = lodash.sortBy(results, sortBy)
    }

    if (sortOrder === 'desc') {
        results.reverse()
    }

    return {
        count: results.length,
        results: results
    }
}

