import { getGlobalState, getGlobalStateCopy, onLoad, resetPersistedState, saveGlobalState } from "../persist.js"
import { apiGetTicketComments } from "./comments.js"
import { normalizeId } from "./helpers.js"
import { apiGetJobById } from "./jobresults.js"
import { apiSearch } from "./search.js"
import { apiTicketsImportCreateMany, apiTicketsShowMany, apiTicketUpdateMany } from "./tickets.js"
import { apiUsersSearchByEmail, apiUsersCreateMany, apiUsersShowMany } from "./users.js"

/*
        1 uri: '/api/v2/users/create_many', // CURLS
            curl -d '{"users":[{"name":"u1", "email":"a@b.com"}]}' -H "Content-Type: application/json" -X POST 'localhost:8999/api/v2/users/create_many'
        2 uri: `/api/v2/users/search?query=email:"${encodeURIComponent(zendeskEmail)}"` // CURLS
            curl 'localhost:8999/api/v2/users/search?query=email:df'
        3 uri: `/api/v2/users/show_many?ids=${ids.join(',')}` // CURLS
            curl 'localhost:8999/api/v2/users/show_many?ids=65565,990140'
        4 uri: '/api/v2/imports/tickets/create_many' // CURLS
            see json in the ./test directory
            curl -d '@./test/curl_import.json' -H "Content-Type: application/json" -X POST 'localhost:8999/api/v2/imports/tickets/create_many'
        5 uri: '/api/v2/tickets/update_many.json' // CURLS
            see json in the ./test directory
            curl -d '@./test/curl_update.json' -H "Content-Type: application/json" -X POST 'localhost:8999/api/v2/tickets/update_many.json'
        6 uri: `/api/v2/tickets/show_many`  // CURLS
            curl 'localhost:8999/api/v2/tickets/show_many?ids=187661'
        7 uri: `/api/v2/tickets/:id/comments`  // CURLS
            curl 'localhost:8999/api/v2/tickets/63849/comments'
        8 uri: `/api/v2/search`
            curl 'http://localhost:8999/api/v2/search.json?query=type:ticket%20-status:closed%20updated%3E2021-11-02%20-tags:tag-to-replace-has-processed%20-custom_field_1260826564690:%22skipThisTicket%22%20-custom_field_1900006024804:%22FromEmail%22&sort_by=created_at&sort_order=desc'
*/

export function apiRoutes(app) {
      const globalState = getGlobalState()
      const register = (method, endpoint, fn)=> {
        app[method](endpoint, fn)
        app[method](endpoint + '.json', fn)
      }

      register('post', '/api/v2/users/create_many', (req, res) => {
        wrapHandler(()=> {
            const result = apiUsersCreateMany(req.body)
            res.send(result)
        }, req, res)
      })

      register('get', '/api/v2/users/search', (req, res) => {
        wrapHandler(()=> {
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
        wrapHandler(()=> {
            if (!req.query.ids) {
                throw errNotImplemented('no ids given')
            }
            const result = apiUsersShowMany(req.query.ids)
            res.send(result)
        }, req, res)
      })

      register('post', '/api/v2/imports/tickets/create_many', (req, res) => {
        wrapHandler(()=> {
            const result = apiTicketsImportCreateMany(req.body)
            res.send(result)
        }, req, res)
      })

      register('post', '/api/v2/tickets/update_many', (req, res) => {
        wrapHandler(()=> {
            const result = apiTicketUpdateMany(req.body)
            res.send(result)
        }, req, res)
      })

    register('get', '/api/v2/tickets/show_many', (req, res) => {
        wrapHandler(()=> {
            if (!req.query.ids) {
                throw errNotImplemented('no ids given')
            }
            const result = apiTicketsShowMany(req.query.ids)
            res.send(result)
        }, req, res)
    })
      
    register('get', '/api/v2/tickets/:id/comments', (req, res) => {
        wrapHandler(()=> {
            if (!req.params.id || !parseInt(req.params.id)) {
                throw errNotImplemented('no ticketid given')
            }
            const ticketId = normalizeId(req.params.id)
            const result = apiGetTicketComments(ticketId)
            res.send(result)
        }, req, res)
      })

      register('get', '/api/v2/search', (req, res) => {
        wrapHandler(()=> {
            const result = apiSearch(req.query.query, req.query.sort_by, req.query.created_at)
            res.send(result)
        }, req, res)
    })

      register('get', '/api/v2/job_statuses/:id', (req, res) => {
        wrapHandler(()=> {
            if (!req.params.id) {
                throw errNotImplemented('no jobid given')
            }
            const jobid = normalizeId(req.params.id.replace('.json', ''))
            const result = apiGetJobById(jobid)
            res.send(result)
        }, req, res)
      })
      
      register('get', `${globalState.globalConfigs.overrideJobStatusUrlPrefix}/api/v2/job_statuses/:id`, (req, res) => {
        wrapHandler(()=> {
            if (!req.params.id) {
                throw errNotImplemented('no jobid given')
            }
            const jobid = normalizeId(req.params.id.replace('.json', ''))
            const result = apiGetJobById(jobid)
            res.send(result)
        }, req, res)
      })
        
      register('post', '/api/delete_all_tickets', (req, res) => {
        wrapHandler(()=> {
            const globalState = getGlobalStateCopy()
            globalState.persistedState.tickets = {}
            globalState.persistedState.comments = {}
            saveGlobalState(globalState)
            res.send({})
        }, req, res)
      })

      register('post', '/api/delete_all', (req, res) => {
        wrapHandler(()=> {
            resetPersistedState()
            onLoad()
            res.send({})
        }, req, res)
      })
}

export function errNotImplemented(s) {
    return new Error(`not implemented: ${s}`)
}

const STATUS_NOT_IMPLEMENTED = 405
const STATUS_BAD_REQUEST = 400
function wrapHandler(fn, req, res) {
    fn(req, res)
    return
    //~ try {
        //~ fn(req, res)
    //~ } catch(e) {
        //~ if (e.message.startsWith('not implemented:')) {
            //~ res.status(STATUS_NOT_IMPLEMENTED).send({error: e.message});
        //~ } else {
            //~ res.status(STATUS_BAD_REQUEST).send({error: e.message});
        //~ }
    //~ }
}
