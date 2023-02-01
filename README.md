# InnoDB Optimize
[![Pypi](https://img.shields.io/pypi/v/innodb-optimize)](https://pypi.org/project/innodb-optimize)
[![MIT licensed](https://img.shields.io/badge/license-MIT-green.svg)](https://raw.githubusercontent.com/Scraps23/innodb_optimize/main/LICENSE)
![GitHub Release Date](https://img.shields.io/github/release-date/Scraps23/innodb_optimize)

`innodb-optimize` is a package for automatically calucalating optimized InnoDB configurations, and generating an updated `my.cnf` file with those values.

## Installation

```bash
# PyPi Installation
pip install innodb-optimize
# GitHub Installation
pip install git+'https://github.com/Scraps23/innodb_optimize.git'
```

## Usage

### Basic Output

The following command will output the generated configuration to `STDOUT`. This is useful when using this tool in other scripts, such as automating system deployments.

```bash
innodb-optimize
```

### Standard Commit Loop

The `--commit` flag should be included for an interactive run.
The user is first asked whether the configuration should be saved; there is an option to print the generated config to console.  
If the configuration is read, the user is prompted for the same question.  
If the configuration is saved, the user is prompted to restart MySQL; there is an option to schedule the restart using bash's `at` program.

```bash
innodb-optimize --commit
```

![Standard Loop](https://user-images.githubusercontent.com/59057336/192899977-148075e7-cc93-43b1-ac3f-b318c507ec9d.PNG)

## Available Arguments

- `file`: Where the MySQL configuration file is located. Defaults to `/etc/mysql/my.cnf`.
- `percent`: Determines what percentage of the total memory will be devoted to InnoDB engine usage. Defaults to 75%.
- `memory`: Allows the user to override the total memory amount (i.e. a fixed amount is already pre-allocated which is not easily accounted for in percentages). Only allows for kilobyte unit.
- `commit`: Is required to start the loop which will commit the changes. Without it, the program only outputs the config to standard out to allow for piping/redirecting the output as needed.
