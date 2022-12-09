
// https://regbrain.com/article/bootstrap-express
// https://www.edureka.co/blog/rest-api-with-node-js/
// Run 'node app' to launch.
import express from 'express';
import http from 'http';
import nunjucks from 'nunjucks';
import path from 'path';
import cors from 'cors';
import sassMiddleware from 'node-sass-middleware';
import { onLoad } from './persist.js';
import { webRoutes } from './web/webroutes.js';
import { apiRoutes } from './api/apiroutes.js';
import { portNumber } from './api/helpers.js';

let app = express()
const rootdir = '.'

// if using nodemon, remember to specify only to watch .js changes
// by default it watches .json changes, rebooting the server on every save,
// which wipes out in-memory state like jobs.

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

app.use(express.urlencoded()) // needed for frontend to communicate
//~ app.use(express.json()) // needed to get post.body
app.use(cors());

onLoad() // call before defining routes

webRoutes(app)
apiRoutes(app)

let server = http.createServer(app)

server.listen(portNumber.toString(), () => {
  console.log(`Listening on port ${portNumber}...`)
})

