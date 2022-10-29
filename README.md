# `tailparse`

Meant to mimic, sort of, how the OG [logparser for MS
Server](https://en.wikipedia.org/wiki/Logparser) worked. 

Very much a work-in-progress atm. Goal is to make this a standalone
python executable for deployment on servers. Will probably have to
change the name to make space on package repos. 

## Installation

`tailparse` has no dependencies to install. It only works with
python 3 and has only been tested in python 3.10. Presumably it would
work as far back as python 3.6.
```
python3 setup.py install --user
```

This will install it in your home directory
(i.e. `home/<username>/.local/bin/`) and doesn't require sudo
privileges. 


## Usage

`tailparse -q <sqlite-query> your.logs`

Help:
```
$ tailparse --help
usage: tailparse [-h] [-p] [-i INPUT_FORMAT] -q QUERY [-r MAX_ROWS] [-s SAVE_DB] LOGS_TO_QUERY

Process some SQL

positional arguments:
  LOGS_TO_QUERY         The path to the input log we're processing. If not present, will use stdin.

options:
  -h, --help            show this help message and exit
  -p, --print           Print out the requisite columns
  -i INPUT_FORMAT, --input-format INPUT_FORMAT
                        The format of the log we're processing. Defaults to 'nginx'. Options include ['nginx']
  -q QUERY, --query QUERY
                        The query to execute. Don't include any 'FROM' statement as this is added automatically.
  -r MAX_ROWS, --max-rows MAX_ROWS
                        Number of max rows to print. Defaults to 20. Put 0 to print all.
  -s SAVE_DB, --save-db SAVE_DB
                        Whether to save the resulting SQLite data file. Defaults to not saving it and using ':memory:'
                        instead. If the database exists, then the log file will not be used to populate it and instead it
                        will be read from. This can be helpful if you're running a lot of queries as the log file doesn't
                        need to be re-parsed everytime.
```


### Caching the database on-disk

It can help to write the SQL database to disk instead of reading from
memory. This can be done with the `-s` or `--save-db` arguments:
```
$ time tailparse -s tmp.sqlite3.db -q "SELECT COUNT(*) FROM logs" sample.logs
['COUNT(*)']
[(100090,)]
real    0m1.038s
user    0m0.850s
sys     0m0.088s
$ time tailparse -s tmp.sqlite3.db -q "SELECT COUNT(*) FROM logs" sample.logs
['COUNT(*)']
[(100090,)]
real    0m0.609s
user    0m0.545s
sys     0m0.064s

# and without any caching
$ time tailparse -q "SELECT COUNT(*) FROM logs" sample.logs
['COUNT(*)']
[(100090,)]
real    0m0.902s
user    0m0.858s
sys     0m0.040s
```

Note that if you do this, `logparser` will not attempt to rewrite the database


## Running Tests

To run tests, at the top level run the following:
```
pip install --user coverage

# at the top directory
coverage run -m unittest
coverage report --omit=*/tests/*
```


## Todos  
  
+ [ ] write [proper
      tests](https://docs.python.org/3/library/unittest.html) 
      
  + [X] split the `logparser.py` file up into separate chunks 
  
  + [ ] `tailparse.execute.execute_query`: write integration tests
        against this and check for the output string -- _all for 'nginx'_
        
    + [ ] include `sample.log` via `shuf -n N input > output`
    + [ ] `SELECT * FROM logs LIMIT 1`
    + [ ] `SELECT * FROM logs LIMIT 2`
    + [ ] `SELECT * FROM logs`: stops at 20 by default
    + [ ] `SELECT * FROM logs`, w/max_rows=0: does not stop at 20
    + [ ] `SELECT *`: complains before it executes
    + [ ] w/`query_file`: write to `/tmp` and clean up after
    + [ ] w/`save_db`: write to `/tmp` and clean up after
    + [ ] w/`save_db`: both with stdin and if its a file
    + [ ] w/`print_columns`: as `True`, should print just columns
    
  + [ ] `tailparse.print_output.print_output`: write unit tests
        against this and check for output string
        
  + [x] write testing shell script -- should fail if `mypy` fails or
        if `coverage` and `mypy` aren't installed

+ [ ] update the README to use current version screenshots

+ [ ] add `--version` argument

+ [ ] write proper contribution guides, especially for new log formats

+ [ ] write proper `Make` file to make it easy for people to see whats
      going on

+ [x] remove pandas dependency and only use pure python

+ [x] support writing to disk for the sqlite3 database, not just to
      memory 

+ [ ] support other formats, not just Nginx
  + [ ] apache 
  + [ ] [morgan](https://www.npmjs.com/package/morgan)

+ [x] Ability to process multiple SQL commands in a text file,
      separated by line
      
+ [ ] infer the table (e.g. `FROM logs`) so I don't have to specify it
      everytime 


## License

[GPL-v3](https://www.gnu.org/licenses/gpl-3.0.en.html)
