#!/usr/bin/env phantomjs

var page = require('webpage').create()
  , system = require('system')
  , fs = require('fs')

if (system.args.length != 3) {
  console.log('USAGE: check-cookies.js [output JSON file] [url]')
  phantom.exit(1)
}

var filename = system.args[1]
  , url = system.args[2]

function f(status) {
  fs.write(filename, JSON.stringify(phantom.cookies) + '\n')
  phantom.exit()
}

page.open(url, f)
