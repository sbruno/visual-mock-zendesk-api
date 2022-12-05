import { errNotImplemented } from "./apiroutes"


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
            throw new Error(`FilterStatus cannot have both include and exclude`)
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
            throw new Error(`FilterByTag cannot have both include and exclude`)
        }

        if (this.includeThese.length) {
            throw new Error('not yet supported')
        } else if (this.excludeThese.length) {
            return (t)=>!t.tags.any(tag => this.excludeThese.includes(tag))
        } else {
            return (t)=>true
        }
    }
}

class FilterCustomField extends BaseFilter {
    getFilter() {
        if (this.includeThese.length && this.excludeThese.length) {
            throw new Error(`FilterCustomField cannot have both include and exclude`)
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

export function goSearch(query, sortBy, sortOrder) {
    sortBy = sortBy || 'created_at'
    sortOrder = sortOrder || 'asc'
    const queryParts = query.split(' ')
    const filterStatus = new FilterStatus()
    const filterTag = new FilterByTag()
    const filterCustomField = new FilterCustomField()
    for (let part of queryParts) {
        part = part.trim()
        if (!part) {
            continue
        } else if (part.startsWith('updated')) {
            if (part === 'updated>2021-11-02') {
                continue
            } else {
                throw errNotImplemented('only supported clause is updated>')
            }
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
            filterCustomField.includeThese.push(s)
        } else if (part.startsWith('-custom_field_')) {
            const s = part.slice('-custom_field_'.length)
            filterCustomField.excludeThese.push(s)
        } 
    }
}


//~ 2021-11-02
