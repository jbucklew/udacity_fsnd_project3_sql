#!/usr/bin/python3

#
# Project 3
#
# Description: This script connects to a postgresql database and executes
#              3 SQL queries to answer these 3 questions:
#
#              1. What are the most popular three articles of all time?
#              2. Who are the most popular article authors of all time?
#              3. On which days did more than 1 percent of requests lead
#                 to errors?
#
#              The results of each query are output to the screen.
#

import psycopg2

DBNAME = "news"


def get3MostPopular(db):
    """ What are the most popular three articles of all time?

        Returns the top 3 articles in a postgresql result set sorted
        by views desc with fields:
        title - the article title
        views - number of views the article received """

    sql = ("select a.title, count(*) as views from articles a, "
           "(select substring(path from 10) as slug from log) l "
           "where a.slug = l.slug group by a.title order by views "
           "desc limit 3;")
    c = db.cursor()
    c.execute(sql)
    return c.fetchall()


def getMostPopularAuthors(db):
    """ Who are the most popular article authors of all time?

        Returns all authors from the authors table in a
        postgresql result set sorted by views desc with fields:
        name - the authors name
        views - the number of view the author received """

    sql = ("select u.name, l.views from authors u, "
           "(select a.author, count(*) as views from articles a, "
           "(select substring(path from 10) as slug from log) l "
           "where a.slug = l.slug group by a.author) l "
           "where u.id=l.author order by views desc;")
    c = db.cursor()
    c.execute(sql)
    return c.fetchall()


def getDaysWithErrors(db):
    """ On which days did more than 1 percent of requests lead to errors?
        An error is considered a 404 NOT FOUND http status code which
        can be found in the log table.

        Returns postgresql result set sorted by percent desc with fields:
        date - date errors occured
        pct - percentage of errors that occurred on the given date """

    sql = ("select time::date as date, "
           "round((sum(case when status='404 NOT FOUND' "
           "then 1 else 0 end)::decimal / count(*)::decimal) * 100.0, 1) "
           "as pct from log group by date "
           "having ((sum(case when status='404 NOT FOUND' "
           "then 1 else 0 end)::decimal / count(*)::decimal) * 100.0) "
           "> 1.0 order by pct desc;")
    c = db.cursor()
    c.execute(sql)
    return c.fetchall()


# connect to database, run reports and print results
db = psycopg2.connect(database=DBNAME)

print("What are the most popular three articles of all time?")
rows = get3MostPopular(db)
for row in rows:
    print("%s - %s views" % (row))

print()
print("Who are the most popular article authors of all time?")
rows = getMostPopularAuthors(db)
for row in rows:
    print("%s - %s views" % (row))

print()
print("On which days did more than 1%% of requests lead to errors?")
rows = getDaysWithErrors(db)
for row in rows:
    print("%s - %s%% errors" % (row))

db.close()
