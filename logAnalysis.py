#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  Displays the most popular articles, authors and days with high error rates

from flask import Flask, request, redirect, url_for
from logAnalysisdb \
    import get_most_popular_articles, \
    get_most_popular_authors, \
    get_high_error_date

app = Flask(__name__)

# HTML template for the forum page
HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>Log Analysis</title>
    <style>
      h1 { text-indent: 30px; }
      ul.data {mergin-left 50px; text-indent: 10px;}
      div.title {}
      div.views {}
    </style>
  </head>
  <body>
    <h1>The most popular three articles all time</h1>
    <ul class=data>
%s
    </ul>
    <h1>The most popular article authors of all time</h1>
    <ul class=data>
%s
    </ul>
    <h1>Days did more than 1%% of requests lead to errors</h1>
    <ul class=data>
%s
    </ul>
  </body>
</html>
'''

# HTML template for an individual query results
POST_POPULAR_ARTICLES = '''\
    <li class=post>
    <span class=title>&#34;%s&#34; — </span>
    <span class=views>%d views</span>
    </li>
'''

POST_POPULAR_AUTHORS = '''\
    <li class=post>
    <span class=title>%s — </span>
    <span class=views>%d views</span>
    </li>
'''

POST_HIGH_ERROR_DATE = '''\
    <li class=post>
    <span class=title>%s — </span>
    <span class=views>%s%%</span>
    </li>
'''


@app.route('/', methods=['GET'])
def main():
    post_popular_articles = "".join(POST_POPULAR_ARTICLES % (title, num)
                                    for title, num in
                                    get_most_popular_articles())
    post_popular_authors = "".join(
        POST_POPULAR_AUTHORS % (name, sum) for name, sum in
        get_most_popular_authors())
    post_high_error_dates = "".join(
        POST_HIGH_ERROR_DATE % (date, fail_rate) for date, fail_rate in
        get_high_error_date())
    html = HTML_WRAP % (
        post_popular_articles, post_popular_authors, post_high_error_dates)
    return html


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
