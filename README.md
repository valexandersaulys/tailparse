# `logparser`

Meant to mimic, sort of, how the OG [logparser for MS
Server](https://en.wikipedia.org/wiki/Logparser)

Very much a work-in-progress atm


## Usage

`python3 logparser.py -q <sqlite-query> your.logs`

Help:
```
$ ./logparser.py --help
usage: logparser.py [-h] [-p] [-i INPUT_FORMAT] -q QUERY [-r MAX_ROWS] [-c MAX_COLS] LOGS_TO_QUERY

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
  -c MAX_COLS, --max-cols MAX_COLS
                        Number of max columns to print. Defaults to 10. Put 0 to print all.
```


## Todos

+ [ ] support other formats, not just Nginx
  + [ ] apache  
  + [ ] [morgan](https://www.npmjs.com/package/morgan)
  
+ [ ] support writing to disk for the sqlite3 database, not just to
      memory
      
+ [ ] write tests 
  + [ ] split the `logparser.py` file up into separate chunks 

+ [ ] Ability to process multiple SQL commands in a text file,
      separated by line
      
+ [ ] infer the table so I don't have to specify it everytime


## License

[GPL-v3](https://www.gnu.org/licenses/gpl-3.0.en.html)
