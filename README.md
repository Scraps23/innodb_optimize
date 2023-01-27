# innodb-optimize
## MySQL Optimizer

This package is meant to be used to automatically optimize mysql configurations for InnoDB engine type databases.


### Installation
```bash
python -m pip install git+'https://github.com/Scraps23/innodb_optimize.git'
```

### Usage

#### Basic Output
```bash
$ python -m innodb_optimize
```

```python
>>> from innodb_optimize.bootstrap.optimize import main as optimize
>>> optimize()
```

#### Standard Commit Loop
```bash
$ python -m innodb_optimize --commit
```

```python
>>> from innodb_optimize.bootstrap.optimize import main as optimize
>>> optimize(commit=True)
```
![Standard Loop](https://user-images.githubusercontent.com/59057336/192899977-148075e7-cc93-43b1-ac3f-b318c507ec9d.PNG)

The `schedule` option allows you to pass a string to be parsed by `at`. The string is passed directly, so any string accepted by `at` will be accepted.

#### Available Options

- file: Where the MySQL configuration file is located. Defaults to `/etc/mysql/my.cnf`.
- percent: Determines what percentage of the total memory will be devoted to InnoDB engine usage. Defaults to 75%.
- memory: Allows the user to override the total memory amount (i.e. a fixed amount is already pre-allocated which is not easily accounted for in percentages). Only allows for kilobyte unit.
- commit: Is required to start the loop which will commit the changes. Without it, the program only outputs the config to standard out to allow for piping/redirecting the output as needed.
