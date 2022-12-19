import { getGlobalState, getGlobalStateCopy, onLoad, resetPersistedState, saveGlobalState } from "../persist.js"
import { apiGetTicketComments } from "./comments.js"
import { normalizeId, errNotImplemented } from "./helpers.js"
import { apiGetJobById } from "./jobresults.js"
import { apiSearch } from "./search.js"
import { apiTicketsImportCreateMany, apiTicketsShowMany, apiTicketUpdateMany } from "./tickets.js"
import { apiUsersSearchByEmail, apiUsersCreateMany, apiUsersShowMany } from "./users.js"

/**
 * Register api routes
 * Creates both the /endpoint and /endpoint.json style registration
 * Unhandled exceptions are mapped to 400 errors
 * (intentionally not 5xx because clients might retry)
 */
export function apiRoutes(app) {
    const globalState = getGlobalState()
    const register = (method, endpoint, fn) => {
        app[method](endpoint, fn)
        app[method](endpoint + '.json', fn)
    }

    register('post', '/api/v2/users/create_many', (req, res) => {
        wrapHandler(() => {
            const result = apiUsersCreateMany(req.body)
            res.send(result)
        }, req, res)
    })

    register('get', '/api/v2/users/search', (req, res) => {
        wrapHandler(() => {
            const query = req.query.query
            if (!query) {
                throw errNotImplemented('no query given')
            }

            if (!query.startsWith('email:')) {
                throw errNotImplemented('query must begin with email')
            }

            const queryEmail = query.slice('email:'.length)
            if (queryEmail.includes(':')) {
                throw errNotImplemented('only currently support querying by email')
            }

            const result = apiUsersSearchByEmail(queryEmail)
            res.send(result)
        }, req, res)
    })

    register('get', '/api/v2/users/show_many', (req, res) => {
        wrapHandler(() => {
            if (!req.query.ids) {
                throw errNotImplemented('no ids given')
            }

            const result = apiUsersShowMany(req.query.ids)
            res.send(result)
        }, req, res)
    })

    register('post', '/api/v2/imports/tickets/create_many', (req, res) => {
        wrapHandler(() => {
            const result = apiTicketsImportCreateMany(req.body)
            res.send(result)
        }, req, res)
    })

    register('post', '/api/v2/tickets/update_many', (req, res) => {
        wrapHandler(() => {
            const result = apiTicketUpdateMany(req.body)
            res.send(result)
        }, req, res)
    })

    register('get', '/api/v2/tickets/show_many', (req, res) => {
        wrapHandler(() => {
            if (!req.query.ids) {
                throw errNotImplemented('no ids given')
            }
            const result = apiTicketsShowMany(req.query.ids)
            res.send(result)
        }, req, res)
    })

    register('get', '/api/v2/tickets/:id/comments', (req, res) => {
        wrapHandler(() => {
            if (!req.params.id || !parseInt(req.params.id)) {
                throw errNotImplemented('no ticketid given')
            }
            const ticketId = normalizeId(req.params.id)
            const result = apiGetTicketComments(ticketId)
            res.send(result)
        }, req, res)
    })

    register('get', '/api/v2/search', (req, res) => {
        wrapHandler(() => {
            if (!req.query.query) {
                throw new Error('must provide a query ' + JSON.stringify(req.query))
            }

            const result = apiSearch(req.query.query, req.query.sort_by, req.query.sort_order)
            res.send(result)
        }, req, res)
    })

    register('get', '/api/v2/job_statuses/:id', (req, res) => {
        wrapHandler(() => {
            if (!req.params.id) {
                throw errNotImplemented('no jobid given')
            }

            const jobid = normalizeId(req.params.id.replace('.json', ''))
            const result = apiGetJobById(jobid)
            res.send(result)
        }, req, res)
    })

    register('get', `${globalState.globalConfigs.overrideJobStatusUrlPrefix}/api/v2/job_statuses/:id`, (req, res) => {
        wrapHandler(() => {
            if (!req.params.id) {
                throw errNotImplemented('no jobid given')
            }

            // we use overrideJobStatusUrlPrefix (mock.zendesk.com), as a workaround
            // just in case clients expect to see the string 'zendesk.com' in the url.
            const jobid = normalizeId(req.params.id.replace('.json', ''))
            const result = apiGetJobById(jobid)
            res.send(result)
        }, req, res)
    })

    register('post', '/api/delete_all_tickets', (req, res) => {
        wrapHandler(() => {
            const globalState = getGlobalStateCopy()
            globalState.persistedState.tickets = {}
            globalState.persistedState.comments = {}
            saveGlobalState(globalState)
            res.send({})
        }, req, res)
    })

    register('post', '/api/delete_all', (req, res) => {
        wrapHandler(() => {
            resetPersistedState()
            onLoad()
            res.send({})
        }, req, res)
    })
}

/**
 * Send a cleaner status output in case of unhandled exceptions
 */
function wrapHandler(fn, req, res) {
    if (enableWhenDebuggingForBetterCallstacks) {
        fn(req, res)
        return
    }

    try {
        fn(req, res)
    } catch (e) {
        if (e.message.startsWith('not implemented:')) {
            res.status(STATUS_NOT_IMPLEMENTED).send({ error: e.message });
        } else {
            res.status(STATUS_BAD_REQUEST).send({ error: e.message });
        }
    }
}

const STATUS_NOT_IMPLEMENTED = 405
const STATUS_BAD_REQUEST = 400
const enableWhenDebuggingForBetterCallstacks = false

