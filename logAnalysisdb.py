# Database code for log analysis
import sys

import psycopg2 as psycopg2


def get_most_popular_articles():
    """
    Accesses to DB and gets the top most viewed article titles and number of
    views.
    :return: list of tuples title and number of views
    """
    try:
        db = psycopg2.connect("dbname=news")
    except psycopg2.Error as e:
        print("Unable to connect!")
        print(e.pgerror)
        print(e.diag.message_detail)
        sys.exit(1)
    else:
        print("Connected!")

    c = db.cursor()
    c.execute("SELECT s.title, COUNT(*) as num "
              "FROM ("
              "SELECT a.title, log.path "
              "FROM log as log "
              "JOIN articles a ON '/article/' || a.slug = log.path) as s "
              "GROUP BY s.title "
              "ORDER BY num DESC "
              "LIMIT 3;")
    rows = c.fetchall()
    db.close()
    return rows


def get_most_popular_authors():
    """
    Accesses to database and gets the most popular authors and their views
    :return: list of tuples author and number of views
    """
    try:
        db = psycopg2.connect("dbname=news")
    except psycopg2.Error as e:
        print("Unable to connect!")
        print(e.pgerror)
        print(e.diag.message_detail)
        sys.exit(1)
    else:
        print("Connected!")

    c = db.cursor()
    c.execute("SELECT authors.name, au.num "
              "FROM (SELECT s.author, COUNT(*) as num "
              "FROM (SELECT a.title, a.author, log.path FROM log as log "
              "JOIN articles a ON '/article/' || a.slug = log.path) as s "
              "GROUP BY s.author "
              "ORDER BY num DESC) as au "
              "JOIN authors authors ON authors.id = au.author;")
    rows = c.fetchall()
    db.close()
    return rows


def get_high_error_date():
    """
    Accesses to database and gets the days where error is more than 1 percent
    :return: list of tuples dates and error rate
    """
    try:
        db = psycopg2.connect("dbname=news")
    except psycopg2.Error as e:
        print("Unable to connect!")
        print(e.pgerror)
        print(e.diag.message_detail)
        sys.exit(1)

    else:
        print("Connected!")
    c = db.cursor()
    c.execute("SELECT a.date, a.fail_rate "
              "FROM ("
              "SELECT s.date as date, "
              "ROUND((f.fails::numeric/s.total::numeric) * 100.0, 1) as "
              "fail_rate "
              "FROM fails as f RIGHT JOIN total s on s.date = f.date) as a "
              "WHERE a.fail_rate >= 1;")
    rows = c.fetchall()
    db.close()
    return rows
