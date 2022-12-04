
// https://regbrain.com/article/bootstrap-express
//https://www.edureka.co/blog/rest-api-with-node-js/
// Run 'node app' to launch.
import express from 'express';
import http from 'http';
import nunjucks from 'nunjucks';
import path from 'path';
import sassMiddleware from 'node-sass-middleware';
//~ let express = require('express')
//~ let http = require('http')
//~ let nunjucks = require('nunjucks')
//~ let path = require('path')
//~ let sassMiddleware = require('node-sass-middleware')

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

app.get('/', function(req, res, next) {
  let  data = {
    content: 'Hello world!',
    title: 'Bootstrap example'
  }

  res.render('index.njk', data)
})

let server = http.createServer(app)

server.listen('8999', () => {
  console.log('Listening on port 8999...')
})

