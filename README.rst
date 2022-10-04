"""""""""""""""
innodb-optimize
"""""""""""""""
...............
MySQL Optimizer
...............

.. contents:: Overview
    :depth: 3



======
Basics
======

This package is intended to automatically optimize MySQL to reduce the room for human error, and the skill/effort required to optimize a MySQL database.

==============

The optimizations focus on three InnoDB values for now:
 - innodb_buffer_pool_size (IPS)
 - innodb_buffer_pool_instances (IPI)
 - innodb_buffer_pool_chunk_size (ICS)

The maths were gathered by following the `reference guide <https://dev.mysql.com/doc/refman/8.0/en/innodb-buffer-pool-resize.html>`_ on MySQL's Official website and are broken down a bit more clearly in the details section at the bottom.


============
Installation
============

The package can be installed with ``pip``, or you can download the distribution from the `GitHub repository <https://github.com/Scraps23/innodb_optimize>`_.

.. code-block::

    $ pip install innodb_optimize


=====
Usage
=====

The package performs a "dry run" by default, and returns the optimized configuration file to STDOUT to allow for piping and capturing in variables.

Otherwise, you can use the ``commit`` flag to enter an interactive loop which allows for a more guided experience.


Parameters
----------

The package currently takes four optional parameters:
 - file
 - percent
 - memory
 - commit

==============

**File**: Defaults to ``/etc/mysql/my.cnf``. Points to the configuration file the target mysql instance runs from.

**Percent**: Defaults to ``75``. Integer that determines what percentage of ``memory`` to use.

**Memory**: Defaults to full system memory. Integer of kb to consider for memory; makes it easy to divide resources (i.e 2GB for Apache2 and 4GB for MySQL) without working in percentages.

`The above flags affect how the package will run no matter what (the current configuration file is read in non-commit mode as well in order to maintain changes), but the flag below is used to change between the default behavior and the commit behavior.`

**Commit**: Begins the loop operation which will **reboot** the MySQL instance *if* the user accepts the prompts.


Default Behavior
----------------

This behavior is meant for developer's and advanced users who are looking to integrate this code in their own projects. It is used by leaving out the ``commit`` flag on runtime.

Here's an example in bash and python showing how to use this output:

.. code:: bash

    python -m innodb_optimize
    # Outputs the optimized configuration file like 'cat' would
    python -m innodb_optimize > /etc/mysql/test_conf.cnf \
        && mysqld --defaults-file=/etc/mysql/test_conf.cnf --validate-config \
        && mv /etc/mysql/test_conf.cnf /etc/mysql/my.cnf \
        && service mysql restart

.. code:: python

    from os import system
    from shutil import move
    from innodb_optimize.bootstrap.optimize import main as optimize

    new_conf = optimize()

    with open('/etc/mysql/test_conf.cnf','w') as stream:
        stream.write(new_conf)
    if system('mysqld --defaults-file=/etc/mysql/test_conf.cnf --validate-config'):
        move('/etc/mysql/test_conf.cnf','/etc/mysql/my.cnf')
        system('service mysql restart')



`As you can see, this behavior will not make any changes to the running MySQL instance, so I had to use other means to affect the desired changes. This can be particularly useful in packages and projects intended to clone running instances' configurations with added optimizations. What you do with the configuration that is output is then up to you to decide.`


Commit Behavior
---------------

The commit behavior is interactive and more guided. The loop behavior is laid out below:

 - Top-level Loop: ``Configuration ready. Commit now?``
 
   * Yes: ``Configuration has been applied. Restart MySQL now?`` 
 
     + Yes: *Restarts mysql and exits the program*
     + No: *Warns user restart will be needed and exits the program*
     + Schedule: *Allows the user to pass a string to * ``at`` * to schedule a restart of mysql*

   * No: *Exits the program*
   * Read: *Outputs optimized configuration to STDOUT for review and restarts top-level loop*

==============

Simply pass the ``commit`` flag on runtime to enter the interactive loop:

.. code:: bash

  python -m innodb_optimize --commit
  Configuration ready. Commit now?
   [y] Yes  [n] No  [r] Read Config : y
  Configuration has been applied. Restart MySQL now?
  [y] Yes  [n] No  [s] Schedule : y
  
.. code:: python

  >>> from optimize import main as optimize
  >>> optimize(commit=True)
  Configuration ready. Commit now?
   [y] Yes  [n] No  [r] Read Config : y
  Configuration has been applied. Restart MySQL now?
  [y] Yes  [n] No  [s] Schedule : s
  Enter time to restart MySQL
  (e.g. tomorrow 10am, now + 30 minutes, etc) : now + 3 minutes
  warning: commands will be executed using /bin/sh
  job 5 at Mon Oct  3 17:11:00 2022
  
