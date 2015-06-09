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

page.open(url)

// https://groups.google.com/d/msg/phantomjs/dEI28sMwGEU/Z8bQXS-fPOUJ
setTimeout(function() {
  setTimeout(function() {          
    fs.write(filename, JSON.stringify(phantom.cookies) + '\n')
//  page.render(filename.replace('.json', '') + '.png')
//  console.log(page.url)
    phantom.exit()
  }, 5000)
}, 1)
