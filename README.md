# Tailparse

[![CodeCov](https://codecov.io/gh/valexandersaulys/tailparse/branch/master/graph/badge.svg)](https://codecov.io/gh/valexandersaulys/tailparse)
[![MIT License](https://img.shields.io/pypi/l/tailparse)](https://pypi.org/project/tailparse/)
[![Support Python Versions](https://img.shields.io/pypi/pyversions/tailparse)](https://pypi.org/project/tailparse/)
[![Wheel Build](https://img.shields.io/pypi/wheel/tailparse)](https://pypi.org/project/tailparse/)
[![PyPi Version](https://img.shields.io/pypi/v/tailparse)](https://pypi.org/project/tailparse/)
[![PyPi Version Status](https://img.shields.io/pypi/status/tailparse)](https://pypi.org/project/tailparse/)

Meant to mimic, sort of, how the OG [logparser for MS
Server](https://en.wikipedia.org/wiki/Logparser) worked. 


## Installation
 
```
$ pip install tailparse

# then check it installed correctly
$ tailparse --version
tailparse v0.2
```

`tailparse` has no dependencies to install. 

See [below](#usage) for examples on how to use.


### Other Ways

Other ways to install. 
```
git clone https://github.com/valexandersaulys/tailparse
python setup.py install --user

# or with pip
pip install git+https://git@github.com/valexandersaulys/tailparse.git#egg=tailparse

# or if you want to actively develop it locally
python setup.py develop  --user
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
`coverage` and [`mypy`](https://mypy.readthedocs.org/en/stable/) are
used to do coverage reports and type checking,
respectively. `./test.sh` will check for these installs at runtime. 


## Contributing

Feel free to make a PR. 

Note that this library is trying very hard to avoid any dependencies
and stay core-python-only. If there is a strong reason to include one,
please include a reason why.  

`black` is used for all code formatting. 

Testing will be required for any contributions. 


## Future Features / Roadmap

(In no particular order)

+ [ ] refactor regexp maker to be a class that other ones inherit from
  + functional programming is a bit preferred but an object would
    guarantee uniformity in how new ones get implemented. 
  
+ [ ] write proper contribution guides, especially for new log formats

+ [ ] support other formats, not just Nginx
  + [ ] apache 
  + [ ] [morgan](https://www.npmjs.com/package/morgan)
      
+ [ ] parse log name into table name, allow for multiple logs to be
      parsed and queried against
      
+ [ ] add universal configuration file
  + creates default tables from existing log files (e.g. nginx access
    logs, systemd logs) 

+ [ ] write test to confirm mismatched logs are ignored

+ [ ] write parser to understand `Key=Value` pairs in a log
  + example: `Ip=192.168.0.1 timeToGet=38s user=JohnnyBoy198`
      
+ [ ] infer the table (e.g. `FROM logs` in the query) so I don't have
      to specify it everytime 
      
+ [ ] add option to convert to JSON for viewing in chrome consoles


## License

[GPL-v3](https://www.gnu.org/licenses/gpl-3.0.en.html)
