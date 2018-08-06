# TF2pdf
This script can extract content from any http://tensorflow.com/api_docs page. If page has another http://tensorflow.com/api_docs 
they will be processed too.

main.py
main.py has main function and some other functions.
  gethtmltextfromlink(link) - gets url and returns text of html page
  startTFRecurcive(htmlbodystring) - function to start recurcive function
  recurciveTFContentExtractor(htmlbodystring, div_name ='', link_dict = {}) - this funcion takes string of a web-page and makes from many html pages with cross-referenced links one big with internal links
  
html_parcer.py
This file has a html_class definition. It has only two methods:
  _init_ - method to create class
  getHTMLString - returnes modified html
And 6 members:
  _prefix, _head, _body, _postfix - parts of html
  _func_head, _func_body - functions to modify parts of html
  
Usage:
main.py --url <link to page> -o <outputfile>
[--css <css file>]
[--page-size <page size to print (A4 for default)>]
!!!Do not use quotes!!!

Algorithm:
1.Creates html_parcer object with html string from gethtmltextfromlink(url) and startTFRecurcive as _func_body
2.Starts getHTMLString which starts a recurcive -> big html string
3.Using pdfkit making pdf
