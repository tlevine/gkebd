#!/usr/bin/env phantomjs
#
# USAGE: check-cookies.js [output JSON file] [url]
#

var page = require('webpage').create()
  , system = require('system')
  , fs = require('fs')

var filename = system.args[1]
  , url = system.args[2]

function f(status) {
  fs.write(filename, JSON.stringify(phantom.cookies))
  phantom.exit()
}

page.open(url, f)
