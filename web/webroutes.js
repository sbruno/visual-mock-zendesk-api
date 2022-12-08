
import { getGlobalState, onLoad, resetPersistedState } from "../persist.js"
import { renderTicketProps } from "./render-object-props.js";

export function webRoutes(app) {
    app.get('/', function(req, res) {
        res.redirect('/web/tickets-open');
      })
    app.get('/web/tickets-open', function(req, res) {
      const globalState = getGlobalState()
        let data = {
          title: 'Open tickets',
          tickets: globalState.persistedState.tickets.filter(t=>t.status !== 'solved' && t.status !== 'closed').map(renderTicketProps)
        }
      
        res.render('homeview.njk', data)
      })
    app.get('/web/tickets-resolved', function(req, res) {
      const globalState = getGlobalState()
      let data = {
        title: 'Resolved tickets',
        tickets: globalState.persistedState.tickets.filter(t=>t.status === 'solved' || t.status === 'closed').map(renderTicketProps)
      }
    
      res.render('homeview.njk', data)
      })
    app.get('/web/tickets-new', function(req, res) {
      const globalState = getGlobalState()
      let data = {
        title: 'New ticket',
        message: globalState.configs.createNotSupportedMessage || "We don't yet support creating a new ticket."
      }
    
      res.render('ticketnew.njk', data)
      })
    app.get('/agent/tickets/:id', function(req, res) {
      if (!req.params.id || !parseInt(req.params.id)) {
          throw errNotImplemented('no ticketid given')
      }
      
      let data = {
        title: `Viewing ticket ${req.params.id}`,
        ticket: renderTicketProps(globalState.persistedState.tickets[req.params.id]),
        comments: renderTicketComments(req.params.id),
      }
    
      res.render('ticketview.njk', data)
      })
}

