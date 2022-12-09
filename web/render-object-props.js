import { getGlobalState } from "../persist.js"
import { renderCustomFields } from "../api/customfields.js"



export function renderTicketProps(t) {
    t = {...t}
    t.custom_fields_rendered = renderCustomFields(t)
    t.created_at_rendered = renderDate(t.created_at)
    t.modified_at_rendered = renderDate(t.modified_at)
    t.requester_rendered = renderUsername(t.requester_id)
    t.tags_rendered = ';'.join(t.tags)
    return t
}

export function renderUsername(userId) {
    const globalState = getGlobalState()
    const user = globalState.persistedState.users[userId]
    if (!user) {
        return '<user not found>'
    }
    return user?.name || '<no name>'
}

export function renderDate(s) {
    try {
        var d = new Date(s)
        return `${d.getFullYear()}/${d.getMonth()}/${d.getDate()}` 
    } catch (e) {
        return '<unknown date>'
    }
}

export function renderTicketComments(tId) {
    const globalState = getGlobalState()
    const t = globalState.persistedState.tickets[tId]
    const result = { 
        comments: t.comment_ids.map(cId => renderTicketComment(cId))
    }

    result.comments = lodash.sortBy(result.comments, c=>new Date(c.created_at)?.valueOf())
    return result
}

export function renderTicketComment(cId) {
    const globalState = getGlobalState()
    let c = globalState.persistedState.comments[cId]
    c = {...c}
    c.created_at_rendered = renderDate(c.created_at)
    c.modified_at_rendered = renderDate(c.modified_at)
    c.requester_rendered = renderUsername(c.author_id)
    return c
}
