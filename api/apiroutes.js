import { searchByEmail } from "./users.js"



export function apiRoutes(app) {
    app.get('/api/v2/users/search', (req, res) => {
        const query = req.query.query
        if (!query) {
            throw Error('no query given')
        }
        if (!query.startsWith('email:')) {
            throw Error('query must begin with email')
        }
        const queryEmail = query.slice('email:'.length)
        if (queryEmail.includes(':')) {
            throw Error('only currently support querying by email')
        }
      
        const result = searchByEmail(queryEmail)
        res.send(result)
      })
}
