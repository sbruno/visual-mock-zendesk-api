import { getGlobalState } from "../persist.js"
import { renderCustomFields } from "../api/customfields.js"
import lodash from 'lodash';



export function renderTicketProps(t) {
    t = {...t}
    t.custom_fields_rendered = renderCustomFields(t)
    t.created_at_rendered = renderDate(t.created_at)
    t.updated_at_rendered = renderDate(t.updated_at)
    t.requester_rendered = renderUsername(t.requester_id, 'name')
    t.requester_email_rendered = renderUsername(t.requester_id, 'email')
    t.tags_rendered = t.tags?.join(';')
    return t
}

export function renderUsername(userId, fld) {
    const globalState = getGlobalState()
    const user = globalState.persistedState.users[userId]
    if (!user) {
        return '<user not found>'
    }
    return user[fld]
}

export function renderDate(s) {
    try {
        var d = new Date(s)
        return `${d.getFullYear()}/${d.getMonth()+1}/${d.getDate()}` 
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
    c.updated_at_rendered = renderDate(c.updated_at)
    c.author_rendered = renderUsername(c.author_id, 'name')
    c.author_email_rendered = renderUsername(c.author_id, 'email')
    return c
}
