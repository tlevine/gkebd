#!/usr/bin/env phantomjs

var webpage = require('webpage')
var system = require('system')

function checkPageCookies(filename, url) {
  var page = webpage.create()
  page.open(url, f)
  function f(status) {
    fs.write(filename, JSON.stringify(phantom.cookies))
  }
}

function main() {
   var filename = system.args[1]
     , url = system.args[2]

  checkPageCookies(filename, url)
}
