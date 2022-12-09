


export function runTriggersOnNewCommentPosted(globalState, ticket, newComment) {
    const triggers = globalState.globalConfigs.customTriggers;
    if (triggers) {
        for (let trigger of triggers) {
            const {action, value} = trigger
            if (action === 'removeTagWhenPublicCommentPosted') {
                removeTagWhenPublicCommentPosted(globalState, ticket, newComment, value)
            } else if (action === 'openPostWhenPublicCommentContainingTextPosted') {
                openPostWhenPublicCommentContainingTextPosted(globalState, ticket, newComment, value)
            } else {
                throw new Error(`unsupported custom trigger ${action}`)
            }
        }
    }
}

function removeTagWhenPublicCommentPosted(globalState, ticket, newComment, value) {
    if (newComment.public) {
        if (ticket.tags?.includes(value)) {
            console.log('Running trigger removeTagWhenPublicCommentPosted')
            ticket.tags = ticket.tags.filter(t=>t !== value)
        }
    }
}

function openPostWhenPublicCommentContainingTextPosted(globalState, ticket, newComment, value) {
    if (newComment.public && (newComment.plain_body?.includes(value) ||newComment.body?.includes(value))) {
        console.log('Running trigger openPostWhenPublicCommentContainingTextPosted')
        ticket.status = 'open'
    }
}

