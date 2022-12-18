

import express from 'express';
import http from 'http';
import nunjucks from 'nunjucks';
import path from 'path';
import sassMiddleware from 'node-sass-middleware';
import { onLoad } from './persist.js';
import { webRoutes } from './web/webroutes.js';
import { apiRoutes } from './api/apiroutes.js';
import { getPortNumber } from './api/helpers.js';

// If using nodemon, remember to specify only to watch .js extension changes.
// By default it watches .json changes too - which is not good because
// we persist state to disk by writing a json, causing many server reboots.
// `nodemon ./app.js -e js` limits to js. 

// Create the express instance
const app = express()
const rootdir = '.'

// Start nunjucks and connect it to express
nunjucks.configure('views', {
  autoescape: true,
  express: app
})

// Start sass
// if indentedSyntax is true, use .sass instead of .scss
app.use(sassMiddleware({
  src: path.join(rootdir, 'bootstrap'),
  dest: path.join(rootdir, 'public'),
  indentedSyntax: true,
  sourceMap: true
}))

// Host static files
app.use(express.static(path.join(rootdir, 'public')))

// Needed, otherwise post.body is not available
app.use(express.json())

// Not needed, server works without this
const useUrlEncoded = false
if (useUrlEncoded) {
    app.use(express.urlencoded())
}

// Not needed, server works without this
const useCors = false
if (useCors) {
    app.use(cors());
}

// Call onLoad before defining the routes
onLoad() 
webRoutes(app)
apiRoutes(app)

// Create the server
const server = http.createServer(app)
server.listen(getPortNumber().toString(), () => {
  console.log(`Listening on port ${getPortNumber()}...`)
})

// References:
// https://regbrain.com/article/bootstrap-express
// https://www.edureka.co/blog/rest-api-with-node-js
