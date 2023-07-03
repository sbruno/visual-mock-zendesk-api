
import assert from "assert";
import yup from 'yup';
import lodash from 'lodash'

import { getCurrentTimestamp } from "./helpers.js";
import { getDefaultAdminId } from "../persist.js";


/**
 * These functions ensure that the data we persist to storage has exactly the correct shape.
 * yup usually permits extra properties but we put things in strict mode here.
 * 
 * The transform* functions generally clean up bad user input, but there are a few cases
 * these functions also currently catch bad input, like malformed dates.
 */

/**
 * Validate a user object
 * (See TypeScript's User.ResponseModel)
 */
export function validateInternalUser(obj) {
    let schema = yup.object({
        id: yup.number().required().positive().integer(),
        name: yup.string().required(),
        email: yup.string().required(),
        created_at: yup.string().required(),
    }).noUnknown(true).required();

    doValidateForInternal(schema, obj)
    checkIsoDateOrThrow(obj.created_at)
    return obj
}

/**
 * Validate a ticket object
 * (See TypeScript's Ticket.ResponseModel)
 */
export function validateInternalTicket(obj) {
    // if you pass a number it will be cast to a string unless you mark the field as strict()
    let schema = yup.object({
        id: yup.number().required().positive().integer(),
        created_at: yup.string().required(),
        updated_at: yup.string().required(),
        // url: not yet implemented
        // external_id: not yet implemented
        // type: not yet implemented
        subject: yup.string().required(),
        raw_subject: yup.string().required(),
        description: yup.string().required(),
        // priority: not yet implemented
        status: yup.string().required(),
        // recipient: not yet implemented
        requester_id: yup.number().required().positive().integer(),
        submitter_id: yup.number().required().positive().integer(),
        assignee_id: yup.number().required().positive().integer(),
        // organization_id: not yet implemented
        // group_id: not yet implemented
        // collaborator_ids: not yet implemented
        // follower_ids: not yet implemented
        // email_cc_ids: not yet implemented
        // forum_topic_id: not yet implemented
        // problem_id: not yet implemented
        // has_incidents: not yet implemented
        // due_at: not yet implemented
        tags: yup.array().of(yup.string()).required(),
        // via: not yet implemented
        custom_fields: yup.array().of(yup.object({
            id: yup.number().required().positive().integer(),
            // NOTE: value may be null
            value: yup.mixed()
        })).required(),
        fields: yup.array().of(yup.object({
            id: yup.number().required().positive().integer(),
            value: yup.mixed().required()
        })).required(),
        // satisfaction_rating: not yet implemented
        // sharing_agreement_ids: not yet implemented
        // followup_ids: not yet implemented
        // ticket_form_id: not yet implemented
        // brand_id: not yet implemented
        // allow_channelback: not yet implemented
        // allow_attachments: not yet implemented
        is_public: yup.bool().required(),
        // comment_count: not yet implemented
        comment_ids: yup.array().of(yup.number()).required(), // not present in Zendesk
    }).noUnknown(true).required();

    doValidateForInternal(schema, obj)
    checkIsoDateOrThrow(obj.created_at)
    checkIsoDateOrThrow(obj.updated_at)
    if (!Statuses.includes(obj.status)) {
        throw new Error(`unsupported status ${obj.status}`)
    }

    return obj
}

/**
 * Validate a comment object
 * (See TypeScript's Comment.ResponseModel)
 */
export function validateInternalComment(obj) {
    let schema = yup.object({
        id: yup.number().required().positive().integer(),
        created_at: yup.string().required(),
        updated_at: yup.string().required(),
        // url: not yet implemented
        type: yup.string().required(), // values are "Comment" | "VoiceComment"
        // request_id: not yet implemented
        body: yup.string().required(),
        html_body: yup.string().required(),
        plain_body: yup.string().required(),
        public: yup.bool().required(),
        author_id: yup.number().required().positive().integer(),
        attachments: yup.array().required(),
        // via: not yet implemented
        // metadata: not yet implemented
    }).noUnknown(true).required();

    doValidateForInternal(schema, obj)
    checkIsoDateOrThrow(obj.created_at)
    checkIsoDateOrThrow(obj.updated_at)
    return obj
}

/**
 * Save a user to the database
 */
export function insertPersistedUser(globalState, obj) {
    validateInternalUser(obj)
    emailCannotExistTwice(globalState, obj.email)
    assert(!globalState.persistedState.users[obj.id], 'user w same id already exists')
    globalState.persistedState.users[obj.id] = obj
}

/**
 * Save a comment to the database
 */
export function insertPersistedComment(globalState, obj) {
    validateInternalComment(obj)
    assert(!globalState.persistedState.comments[obj.id], 'comment w same id already exists')
    globalState.persistedState.comments[obj.id] = obj
}

/**
 * Save a ticket to the database
 */
export function insertPersistedTicket(globalState, obj) {
    validateInternalTicket(obj)
    assert(!globalState.persistedState.tickets[obj.id], 'ticket w same id already exists')
    globalState.persistedState.tickets[obj.id] = obj
}

/**
 * Update a ticket to the database
 */
export function updatePersistedTicket(globalState, obj) {
    validateInternalTicket(obj)
    assert(globalState.persistedState.tickets[obj.id], 'ticket w same id not exists')
    globalState.persistedState.tickets[obj.id] = obj
}

/**
 * Dates in the db should be strings in ISO-8601 format, see getCurrentTimestamp()
 */
function checkIsoDateOrThrow(s) {
    if (!s) {
        throw new Error('not an iso date ' + s)
    } else if (!s.includes('T')) {
        // Do not throw, accept this as long as the parse below succeeds
        console.log('does not contain a T, might not be an iso date' + s)
    }

    try {
        const d = new Date(s)
        assert(d instanceof Date && !isNaN(d), 'date could not be parsed')
    } catch (e) {
        throw new Error('failed to parse iso date ' + s + e)
    }
}

/**
 * Throw if attempt to add same email twice
 */
function emailCannotExistTwice(globalState, email) {
    const allUsers = globalState.persistedState.users
    for (let userId in allUsers) {
        const user = allUsers[userId]
        if (user.email === email) {
            assert(false, 'user with this email already exists ' + email)
        }
    }
}

/**
 * Set yup parameters to make it a stricter comparison
 */
function doValidateForInternal(schema, obj) {
    // stripUnknown: throws if any required are not there
    // strict: do not 'parse', important because internally we want to enforce the int/str distinction,
    // for example, when getting data from outside, we'll accept either a string or int for id,
    // but when persisting in db, always store int ids and we need strict:true to actually enforce that. 
    schema.validateSync(obj, { stripUnknown: false, strict: true })
}

/**
 * Values for status. hold isn't enabled by default iirc.
 */
export const Statuses = ["new", "open", "pending", "hold", "solved", "closed"]
