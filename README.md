# Tailparse

[![CodeCov](https://codecov.io/gh/valexandersaulys/tailparse/branch/master/graph/badge.svg)](https://codecov.io/gh/valexandersaulys/tailparse)
[![MIT License](https://img.shields.io/pypi/l/tailparse)](https://pypi.org/project/tailparse/)
[![Support Python Versions](https://img.shields.io/pypi/pyversions/tailparse)](https://pypi.org/project/tailparse/)
[![Wheel Build](https://img.shields.io/pypi/wheel/tailparse)](https://pypi.org/project/tailparse/)
[![PyPi Version](https://img.shields.io/pypi/v/tailparse)](https://pypi.org/project/tailparse/)
[![PyPi Version Status](https://img.shields.io/pypi/status/tailparse)](https://pypi.org/project/tailparse/)

Meant to mimic, sort of, how the OG [logparser for MS
Server](https://en.wikipedia.org/wiki/Logparser) worked. 

Very much a work-in-progress atm. Goal is to make this a standalone
python executable for deployment on servers. Will probably have to
change the name to make space on package repos. 

## Installation

`tailparse` has no dependencies to install. It only works with
python 3 and has only been tested in python 3.10. Presumably it would
work with any python 3. 
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
usage: tailparse [-h] [-p] [-i INPUT_FORMAT] [-q QUERY] [-r MAX_ROWS] [-s SAVE_DB] [-f FILE] [logs]

Process logs as if they were SQL.

positional arguments:
  logs                  The path to the input log we're processing. If not present, will use stdin.

options:
  -h, --help            show this help message and exit
  -p, --print           Print out the requisite columns
  -i INPUT_FORMAT, --input-format INPUT_FORMAT
                        The format of the log we're processing. Defaults to 'nginx'. Options include ['nginx']
  -q QUERY, --query QUERY
                        The query to execute. Don't include any 'FROM' statement as this is added automatically. If not
                        included, make sure to include a -f/--file arugmenet
  -r MAX_ROWS, --max-rows MAX_ROWS
                        Number of max rows to print. Defaults to 20. Put 0 to print all.
  -s SAVE_DB, --save-db SAVE_DB
                        Whether to save the resulting SQLite data file. Defaults to not saving it and using ':memory:'
                        instead. If the database exists, then the log file will not be used to populate it and instead it
                        will be read from. This can be helpful if you're running a lot of queries as the log file doesn't
                        need to be re-parsed everytime.
  -f FILE, --file FILE  Execute multiple queries contained with a file. Can be used in place of -q/--query
```


### Caching the database on-disk

It can help to write the SQL database to disk instead of reading from
memory. This can be done with the `-s` or `--save-db` arguments:
```
$ time tailparse -s tmp.sqlite3.db -q "SELECT COUNT(*) FROM logs" sample.logs
COUNT(*)
100090

real    0m1.026s
user    0m0.835s
sys     0m0.117s
$ time tailparse -s tmp.sqlite3.db -q "SELECT COUNT(*) FROM logs" sample.logs
COUNT(*)
100090

real    0m0.648s
user    0m0.533s
sys     0m0.095s

# and without any caching
$ time tailparse -q "SELECT COUNT(*) FROM logs" sample.logs
COUNT(*)
100090

real    0m0.910s
user    0m0.866s
sys     0m0.045s
```

Note that if you do this, `tailparse` will not attempt to rewrite the database


## Running Tests

To run tests, at the top level run the following:
```
./test.sh
```

To get coverage reports, which requires the [`coverage`
module](https://coverage.readthedocs.io/en/6.5.0/), you can run:
```
./test.sh -h
```

While testing relies entirely on `unittest`, which is built-in,
`coverage` and `mypy` are used to do coverage reports and type
checking, respectively. `./test.sh` will check for these installs at
runtime.  


## Contributing

Feel free to make a PR! 

Note that this library is trying very hard to avoid any dependencies
and stay core-python-only. If there is a strong reason to include one,
please include a reason why.  

`black` is used for all code formatting. Testing will be required for
any contributions. 


## Todos  
  
+ [ ] write [proper
      tests](https://docs.python.org/3/library/unittest.html) 
      
  + [X] split the `logparser.py` file up into separate chunks 
  
  + [ ] `tailparse.execute.execute_query`: write integration tests
        against this and check for the output string -- _all for 'nginx'_
        
    + [x] include `sample.log` via `shuf -n N input > output`
    + [x] `SELECT * FROM logs LIMIT 1`
    + [x] `SELECT * FROM logs LIMIT 2`
    + [x] `SELECT * FROM logs`: stops at 20 by default
    + [x] `SELECT * FROM logs`, w/max_rows=0: does not stop at 20
    + [x] `SELECT *`: complains before it executes
    + [x] w/`query_file`: write to `/tmp` and clean up after
    + [x] w/`save_db`: write to `/tmp` and clean up after
    + [x] w/`print_columns`: as `True`, should print just columns
    
  + [x] `tailparse.print_output.print_output`: write unit tests
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
