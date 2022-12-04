

export function webRoutes(app) {
    app.get('/', function(req, res) {
        let data = {
          ticketMessage: 'Hello world!2',
          obj: {abc: 'ooo'}
        }
      
        res.render('homeview.njk', data)
      })
}
