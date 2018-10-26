# Database code for log analysis


import psycopg2 as psycopg2


def get_most_popular_articles():
    """
    Accesses to DB and gets the top most viewed article titles and number of
    views.
    :return: list of tuples title and number of views
    """
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("SELECT a.title, v.num "
              "FROM ("
              "SELECT SUBSTRING(path FROM '/article/#\"%#\"' FOR '#') as sub, "
              "COUNT(*) as num "
              "FROM log "
              "WHERE path LIKE '/article/%' "
              "GROUP BY PATH "
              "ORDER BY num DESC LIMIT 3) as v "
              "JOIN articles a ON a.slug = v.sub;")
    rows = c.fetchall()
    db.close()
    return rows


def get_most_popular_authors():
    """
    Accesses to database and gets the most popular authors and their views
    :return: list of tuples author and number of views
    """
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("SELECT au.name, sum(s.num) as sum "
              "FROM (SELECT a.title, a.author, v.num "
              "FROM ("
              "SELECT SUBSTRING(path FROM '/article/#\"%#\"' FOR '#') as sub, "
              "COUNT(*) as num "
              "FROM log "
              "WHERE path LIKE '/article/%' "
              "GROUP BY PATH ORDER BY num DESC) as v "
              "JOIN articles a ON a.slug = v.sub) as s "
              "JOIN authors au ON au.id = s.author "
              "GROUP BY au.name "
              "ORDER BY sum DESC;")
    rows = c.fetchall()
    db.close()
    return rows


def get_high_error_date():
    """
    Accesses to database and gets the days where error is more than 1 percent
    :return: list of tuples dates and error rate
    """
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("SELECT a.date, a.fail_rate "
              "FROM ("
              "SELECT s.date as date, "
              "ROUND((f.fails::numeric/ s.total::numeric) * 100.0, 1) as "
              "fail_rate "
              "FROM fails as f RIGHT JOIN total s on s.date = f.date) as a "
              "WHERE a.fail_rate >= 1;")
    rows = c.fetchall()
    db.close()
    return rows
