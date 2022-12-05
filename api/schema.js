
import assert from "assert";
import yup from 'yup';
import { supportedStatuses } from './status';
export function validateInternalUser(obj) {
    let schema = yup.object({
        id: yup.number().required().positive().integer(),
        name: yup.string().required(),
        email: yup.string().required(),
        created_at: yup.string().required(),
      }).noUnknown(true).required();
      schema.validate(obj, {stripUnknown: false}) // throws if any required are not there
      checkIsoDateOrThrow(obj.created_at)
      return obj
}

export function validateIncomingUserParams(obj) {
    assert(!obj.id, `new user - cannot specify id`)
    let schema = yup.object({
        name: yup.string().required(),
        email: yup.string().required(),
      }).noUnknown(true).required();
      schema.validate(obj, {stripUnknown: true}) // does not throw if any required are not there
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

export function validateInternalTicket(obj) {
    let schema = yup.object({
        id: yup.number().required().positive().integer(),
        created_at: yup.string().required(),
        modified_at: yup.string().required(),
        subject: yup.string().required(),
        raw_subject: yup.string().required(),
        status: yup.string().required(),
        requester_id: yup.number().required().positive().integer(),
        submitter_id: yup.number().required().positive().integer(),
        tags: yup.array().of(yup.string()).required(),
        is_public: yup.bool().required(),
        custom_fields: yup.array().required(),
        fields: yup.object().required(),
        comment_ids: yup.array().of(yup.number()).required(),
    }).noUnknown(true).required();
    schema.validate(obj, {stripUnknown: false}) // throws if any required are not there
    checkIsoDateOrThrow(obj.created_at)
    checkIsoDateOrThrow(obj.modified_at)
    if (!supportedStatuses[obj.status]) {
        throw new Error(`unsupported status ${obj.status}`)
    }
    return obj
}

export function validateIncomingTicketParams(obj) {
    if (obj?.comments?.any(comment=>comment.attachment_ids?.length)) {
        throw new Error("We don't yet support attachments")
    }
    let schemaComment = yup.object({
        created_at: yup.string().optional(),
        body: yup.string().required(),
        public: yup.bool().optional(),
        author_id: yup.number().optional(),
    }).noUnknown(true)
    
    assert(!obj.id, `new ticket - cannot specify id`)
    let schema = yup.object({
        created_at: yup.string().optional(),
        subject: yup.string().optional(),
        status: yup.string().optional(),
        requester_id: yup.string().required(),
        submitter_id: yup.string().optional(),
        submitter_id: yup.string().optional(),

    })

}

export function validateInternalComment(obj) {
    let schema = yup.object({
        id: yup.number().required().positive().integer(),
        created_at: yup.string().required(),
        modified_at: yup.string().required(),
        body: yup.string().required(),
        html_body: yup.string().required(),
        plain_body: yup.string().required(),
        public: yup.bool().required(),
        author_id: yup.number().required().positive().integer(),
        attachment_ids: yup.array().of(yup.number()).required(),
    }).noUnknown(true).required();
    schema.validate(obj, {stripUnknown: false}) // throws if any required are not there
    checkIsoDateOrThrow(obj.created_at)
    checkIsoDateOrThrow(obj.modified_at)
    return obj
}

export function validateInternalAttachment(obj) {
    let schema = yup.object({
        id: yup.number().required().positive().integer(),
        created_at: yup.string().required(),
        content_type: yup.string().required(),
    }).noUnknown(true).required();
    schema.validate(obj, {stripUnknown: false}) // throws if any required are not there
    return obj
}

