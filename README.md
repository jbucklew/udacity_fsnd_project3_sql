# SQL Reports

## Description:
This is a python command line script that will connect to a Postgresql database and run 3 queries against it printing the results.

## Requirements:
* Python 3 - This script is executed from the command line.  If python3 is not in the path /usr/bin you will need to update the first line of the script to the correct path.
* The news database containing the tables articles, authors and log. This database is not provided.

## To Run Application:
* Download the reports.py file to the same host as the Postgresql server.
* Run the script from the command prompt.

## Sites Used:
* [Postgresql Documentation](https://www.postgresql.org/docs/)
* [Stackoverflow](https://stackoverflow.com/)
    * Discovered casting, ::date and ::decimal, that I used in my SQL statements.
    * Help with making the third query more efficient.
