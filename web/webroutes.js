
import { getGlobalState, onLoad, resetPersistedState } from "../persist.js"
import { renderTicketComment, renderTicketComments, renderTicketProps } from "./render-object-props.js";
import lodash from 'lodash';

/**
 * Show html UI for the web endpoints.
 * Nunjucks expands the template with the given parameters.
 */
export function webRoutes(app) {
    app.get('/', function(req, res) {
        res.redirect('/web/tickets-open');
      })

    app.get('/web/tickets-open', function(req, res) {
        let data = {
          title: 'Open tickets',
          tickets: getRenderedTickets(req, res, t=>t.status !== 'solved' && t.status !== 'closed')
        }
      
        res.render('homeview.njk', data)
      })

    app.get('/web/tickets-resolved', function(req, res) {
      let data = {
        title: 'Resolved tickets',
          tickets: getRenderedTickets(req, res, t=>t.status === 'solved' || t.status === 'closed')
      }
    
      res.render('homeview.njk', data)
      })

    app.get('/web/tickets-new', function(req, res) {
      const globalState = getGlobalState()
      let data = {
        title: 'New ticket',
        message: globalState.globalConfigs.createNotSupportedMessage || "We don't yet support creating a new ticket."
      }
    
      res.render('ticketnew.njk', data)
      })

    app.get('/agent/tickets/:id', function(req, res) {
      const globalState = getGlobalState()
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

/**
 * Take a list of tickets and call renderTicketProps on them, to get everything needed to display to the user.
 * For example, turn the list of the comment ids into the actual comment text, and turn the requester id into the requester name. 
 */
function getRenderedTickets(req, res, ticketFilter) {
      const globalState = getGlobalState()
      const results = Object.values(globalState.persistedState.tickets).filter(ticketFilter).map(renderTicketProps)
      return lodash.sortBy(results, t=>new Date(t.created_at)?.valueOf())
}
