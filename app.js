
// https://regbrain.com/article/bootstrap-express
// https://www.edureka.co/blog/rest-api-with-node-js/
// Run 'node app' to launch.
import express from 'express';
import http from 'http';
import nunjucks from 'nunjucks';
import path from 'path';
import sassMiddleware from 'node-sass-middleware';
import { onLoad } from './persist.js';
import { webRoutes } from './webroutes.js';
import { apiRoutes } from './api/apiroutes.js';

let app = express()
const rootdir = '.'

nunjucks.configure('views', {
  autoescape: true,
  express: app
})

app.use(sassMiddleware({
  src: path.join(rootdir, 'bootstrap'),
  dest: path.join(rootdir, 'public'),
  indentedSyntax: true, // true = .sass and false = .scss
  sourceMap: true
}))

app.use(express.static(path.join(rootdir, 'public')))

webRoutes(app)
apiRoutes(app)

let server = http.createServer(app)

server.listen('8999', () => {
  console.log('Listening on port 8999...')
})

onLoad()
