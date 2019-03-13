#! /bin/bash

pip install -r requirements.txt

## check env vars
[ -z "$PGDB" ]              && export PGDB="postgres"
[ -z "$PGUSERNAME" ]        && export PGUSERNAME="postgres"
[ -z "$PGPASSWORD" ]        && export PGPASSWORD="admin"
[ -z "$PGHOST" ]            && export PGHOST="localhost"
[ -z "$PGPORT" ]            && export PGPORT="5432"
[ -z "$NFLDBSTARTYEAR" ]    && export NFLDBSTARTYEAR=2010
[ -z "$NFLDBENDYEAR" ]      && export NFLDBENDYEAR=2019
[ -z "$NFLSUBDB" ]          && export NFLSUBDB="nflDb"
[ -z "$FLASK_APP" ]         && export FLASK_APP="frontend.py"

echo 'Make a choice:'
echo '    1. Intial DB setup (WARNING THIS TAKES A LONG TIME ONLY RUN ONCE!)'
echo '    2. Run front end'
read USERCHOICE

if [ "$USERCHOICE" -eq 1 ]; then
    cd setup
    python db_init.py
elif [ "$USERCHOICE" -eq 2 ] then
    # flask
else
    echo "Invalid Choice"
fi