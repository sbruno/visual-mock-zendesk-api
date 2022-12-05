
import yup from 'yup';
export function validateInternalUser(obj) {
    let schema = yup.object({
        id: yup.number().required().positive().integer(),
        name: yup.string().required(),
        email: yup.string().required(),
        created_at: yup.string().required(),
      }).noUnknown(true).required();
      schema.validate(obj, {stripUnknown: false}) // throws if any required are not there
      return obj
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
        tags: yup.array().of(yup.string()),
        is_public: yup.bool(),
        custom_fields: yup.array(),
        fields: yup.object(),
        comment_ids: yup.array().of(yup.number()),
    }).noUnknown(true).required();
    schema.validate(obj, {stripUnknown: false}) // throws if any required are not there
    return obj
}

export function validateInternalComment(obj) {
    let schema = yup.object({
        id: yup.number().required().positive().integer(),
        created_at: yup.string().required(),
        modified_at: yup.string().required(),
        body: yup.string().required(),
        html_body: yup.string().required(),
        plain_body: yup.string().required(),
        public: yup.bool(),
        author_id: yup.number().required().positive().integer(),
        attachment_ids: yup.array().of(yup.number()),
    }).noUnknown(true).required();
    schema.validate(obj, {stripUnknown: false}) // throws if any required are not there
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

