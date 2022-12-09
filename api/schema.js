
import assert from "assert";
import yup from 'yup';
import lodash from 'lodash'

import { getCurrentTimestamp } from "./helpers.js";
import { supportedStatuses } from './status.js';
export function validateInternalUser(obj) {
    let schema = yup.object({
        id: yup.number().required().positive().integer(),
        name: yup.string().required(),
        email: yup.string().required(),
        created_at: yup.string().required(),
      }).noUnknown(true).required();
      schema.validate(obj, {stripUnknown: false, strict:true}) // throws if any required are not there
      checkIsoDateOrThrow(obj.created_at)
      return obj
}

export function validateIncomingUserParams(obj) {
    assert(!obj.id, `new user - cannot specify id`)
    let schema = yup.object({
        name: yup.string().required(),
        email: yup.string().required(),
      }).noUnknown(true).required();
      schema.validate(obj, {stripUnknown: false, strict:true}) // does not throw if any required are not there
      return obj
}

function checkIsoDateOrThrow(s) {
    if (!s) {
        throw new Error('not an iso date '+s)
    }else if (!s.includes('T')) {
        throw new Error('does not contain a T, might not be an iso date'+s)
    }
    try {
        const d = new Date(s)
    } catch(e) {
        throw new Error('failed to parse iso date ' + s + e)
    }
}

// type Status = "new" | "open" | "pending" | "hold" | "solved" | "closed";


export function transformIncomingTicketUpdateIntoInternal(existing, incomingUpdate) {
    if (incomingUpdate.subject) {
        existing.subject = incomingUpdate.subject
    }
    if (incomingUpdate.requester_id||incomingUpdate.assignee_id||incomingUpdate.assignee_email||
        incomingUpdate.group_id||incomingUpdate.organization_id||incomingUpdate.collaborator_ids ||
        incomingUpdate.additional_collaborators||incomingUpdate.followers||incomingUpdate.priority||incomingUpdate.email_ccs) {
        throw new Error("cannot update this property, not yet implemented")
    }
    if (incomingUpdate.status) {
        existing.status = incomingUpdate.status
    }
    if (incomingUpdate.additional_tags) { // less documented, but does work on latest api
        assert(Array.isArray(incomingUpdate.additional_tags), 'additional_tags must be an array')
        existing.tags = [...existing.tags, ...incomingUpdate.additional_tags]
        existing.tags = lodash.uniq(existing.tags)
    }
    if (incomingUpdate.remove_tags) { // less documented, but does work on latest api
        assert(Array.isArray(incomingUpdate.remove_tags), 'remove_tags must be an array')
        existing.tags = existing.tags.filter(t=>!incomingUpdate.remove_tags.includes(t))
    }
    if (incomingUpdate.tags) {
        existing.status = incomingUpdate.tags
    }
    if (incomingUpdate.external_id||incomingUpdate.problem_id||incomingUpdate.due_at||
        incomingUpdate.updated_stamp||incomingUpdate.sharing_agreement_ids||incomingUpdate.macro_ids ||
        incomingUpdate.attribute_value_ids) {
        throw new Error("cannot update this property, not yet implemented")
    }
    // ignore safe_update for now, would be good to implement in the future for testing race conditions
    fghfgh
    if (incomingUpdate.custom_fields) {
        existing.custom_fields = incomingUpdate.custom_fields
    }

    existing.modified_at = getCurrentTimestamp()
}

export function validateInternalTicket(obj) {
    // if you pass a number it will be cast to a string unless you mark the field as strict()
    let schema = yup.object({
        id: yup.number().required().positive().integer(),
        created_at: yup.string().required(),
        modified_at: yup.string().required(),
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
            value: yup.mixed().required()})).required(),
        fields: yup.array().of(yup.object({
            id: yup.number().required().positive().integer(),
            value: yup.mixed().required()})).required(),
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
    schema.validate(obj, {stripUnknown: false, strict:true}) // throws if any required are not there
    checkIsoDateOrThrow(obj.created_at)
    checkIsoDateOrThrow(obj.modified_at)
    if (!supportedStatuses[obj.status]) {
        throw new Error(`unsupported status ${obj.status}`)
    }
    return obj
}

//~ export function validateIncomingTicketParams(obj) {
    //~ if (obj?.comments?.any(comment=>comment.attachment_ids?.length)) {
        //~ throw new Error("We don't yet support attachments")
    //~ }
    //~ let schemaComment = yup.object({
        //~ created_at: yup.string().optional(),
        //~ body: yup.string().required(),
        //~ public: yup.bool().optional(),
        //~ author_id: yup.number().optional(),
    //~ }).noUnknown(true)
    
    //~ assert(!obj.id, `new ticket - cannot specify id`)
    //~ let schema = yup.object({
        //~ created_at: yup.string().optional(),
        //~ subject: yup.string().optional(),
        //~ status: yup.string().optional(),
        //~ requester_id: yup.string().required(),
        //~ submitter_id: yup.string().optional(),
        //~ submitter_id: yup.string().optional(),

    //~ })

//~ }


export function transformIncomingCommentIntoInternal(obj) {
    if (obj.uploads || obj.attachments) {
        throw new Error('we do not yet support attachments')
    }
    return {
        id: parseInt(obj.id),
        created_at: obj.created_at || getCurrentTimestamp(),
        modified_at: (obj.modified_at || obj.created_at) || getCurrentTimestamp(),
        type: "Comment",
        body: obj.body || obj.html_body,
        html_body: obj.body || obj.html_body,
        plain_body: obj.body || obj.html_body, // just for simplicity
        public: obj.public === undefined ? true : obj.public,
        author_id: obj.author_id,
        attachments: []
    }
}

export function validateInternalComment(obj) {
    let schema = yup.object({
        id: yup.number().required().positive().integer(),
        created_at: yup.string().required(),
        modified_at: yup.string().required(),
        // url: not yet implemented
        type: yup.string().required(), // "Comment" | "VoiceComment"
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
    schema.validate(obj, {stripUnknown: false, strict:true}) // throws if any required are not there
    checkIsoDateOrThrow(obj.created_at)
    checkIsoDateOrThrow(obj.modified_at)
    return obj
}
