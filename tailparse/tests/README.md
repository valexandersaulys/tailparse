# Testing

While `coverage` and `mypy` are used, the testing exclusively relies
on python's built-in `unittest` to process everything. 

Testing does not check if the various SQL queries are at all
correct. The `sqlite` library, both for Python and on the host
machine, is trusted to work as described. 
