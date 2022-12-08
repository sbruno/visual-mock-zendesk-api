import { getGlobalState, onLoad, resetPersistedState } from "../persist.js"
import { getTicketComments } from "./comments.js"
import { getJobById } from "./jobresults.js"
import { importCreateMany } from "./tickets.js"
import { searchByEmail, usersCreateMany, usersShowMany } from "./users.js"

/*
        uri: '/api/v2/users/create_many', // CURLS
        uri: `/api/v2/users/search?query=email:"${encodeURIComponent(zendeskEmail)}"`
        uri: `/api/v2/users/show_many?ids=${ids.join(',')}` // CURLS
        uri: '/api/v2/imports/tickets/create_many' ,
        uri: '/api/v2/tickets/update_many.json',
        uri: `/api/v2/tickets/show_many?ids=${ticketIds.join(',')}`
        uri: `/api/v2/tickets/${ticketId}/comments`,
        uri: `/api/v2/uploads?filename=${encodeURIComponent(filename)}`,
        `/api/v2/search.json?query=type:ticket`;
        job_statuses

*/

export function apiRoutes(app) {
    app.get('/api/v2/users/search', (req, res) => {
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
        
            const result = searchByEmail(queryEmail)
            res.send(result)
        }, req, res)
      })
    app.post('/api/v2/users/create_many', (req, res) => {
        wrapHandler(()=> {
            const result = usersCreateMany(req.body)
            res.send(result)
        }, req, res)
      })
    app.get('/api/v2/users/show_many', (req, res) => {
        wrapHandler(()=> {
            if (!req.query.ids) {
                throw errNotImplemented('no ids given')
            }
            const result = usersShowMany(req.query.ids)
            res.send(result)
        }, req, res)
      })
    app.post('/api/v2/imports/tickets/create_many', (req, res) => {
        wrapHandler(()=> {
            const result = importCreateMany(req.body)
            res.send(result)
        }, req, res)
      })
    app.get('/api/v2/tickets/:id/comments', (req, res) => {
        wrapHandler(()=> {
            if (!req.params.id || !parseInt(req.params.id)) {
                throw errNotImplemented('no ticketid given')
            }
            const ticketId = parseInt(req.params.id)
            const result = getTicketComments(ticketId)
            res.send(result)
        }, req, res)
      })
        app.get('/api/v2/job_statuses/:id', (req, res) => {
        wrapHandler(()=> {
            if (!req.params.id) {
                throw errNotImplemented('no jobid given')
            }
            const jobid = req.params.id.replace('.json', '')
            const result = getJobById(jobid)
            res.send(result)
        }, req, res)
      })
      const globalState = getGlobalState()
      app.get(`${globalState.globalConfigs.overrideJobStatusUrlPrefix}/api/v2/job_statuses/:id`, (req, res) => {
        wrapHandler(()=> {
            if (!req.params.id) {
                throw errNotImplemented('no jobid given')
            }
            const jobid = req.params.id.replace('.json', '')
            const result = getJobById(jobid)
            res.send(result)
        }, req, res)
      })
      app.post('/api/delete_all', (req, res) => {
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
    //~ try {
        fn(req, res)
    //~ } catch(e) {
        //~ if (e.message.startsWith('not implemented:')) {
            //~ res.status(STATUS_NOT_IMPLEMENTED).send({error: e.message});
        //~ } else {
            //~ res.status(STATUS_BAD_REQUEST).send({error: e.message});
        //~ }
    //~ }
}
