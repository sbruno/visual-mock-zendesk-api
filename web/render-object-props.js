import { getGlobalState } from "../persist.js"
import { renderCustomFields } from "../api/customfields.js"
import lodash from 'lodash';

/**
 * Take a ticket object and add some properties, to get everything needed to display to the user.
 */
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

/**
 * Take a user id and add get a rendered user name.
 */
export function renderUsername(userId, fld) {
    const globalState = getGlobalState()
    const user = globalState.persistedState.users[userId]
    if (!user) {
        return '<user not found>'
    }

    return user[fld]
}

/**
 * Take an iso-formatted date and show it in a more friendly way.
 */
export function renderDate(s) {
    try {
        var d = new Date(s)
        return `${d.getFullYear()}/${d.getMonth()+1}/${d.getDate()}` 
    } catch (e) {
        return '<unknown date>'
    }
}

/**
 * Get the comments on a ticket, to get everything needed to display to the user.
 */
export function renderTicketComments(tId) {
    const globalState = getGlobalState()
    const t = globalState.persistedState.tickets[tId]
    const result = { 
        comments: t.comment_ids.map(cId => renderTicketComment(cId))
    }

    result.comments = lodash.sortBy(result.comments, c=>new Date(c.created_at)?.valueOf())
    return result
}

/**
 * Take a comment object and add some properties, to get everything needed to display to the user.
 */
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
