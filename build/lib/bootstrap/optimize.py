#!/usr/bin/python3

from subprocess import check_output, CalledProcessError
from os.path import exists
from os import _exit
from sys import argv
from os import system
import fire

__version__ = '0.1.4'
    
if exists('/etc/apt'): # apt handling
    try:
        check_output('dpkg -l | grep -q "ii  at"', shell=True)
    except CalledProcessError:
        system('apt-get install at -y > /dev/null')
elif exists('/etc/yum.d'): # yum handling
    try:
        check_output('yum list installed at', shell=True)
    except CalledProcessError:
        system('yum install at -y > /dev/null')

def main(memory=None, percent=75, file='/etc/mysql/my.cnf', commit=False):
    def calc_pool_size(memory, percent):
        counter = memory
        while True:
            counter -= 1
            if (((counter * 1000 * 1000) * (percent / 100)) % 1 == 0) and (((counter * 1000) * 0.75) % 1 == 0):
                return int(counter * 1000)

    def calc_pool_dependents(pool_size):
        for instances in range(2, 1001):
            chunk_size = pool_size / instances
            chunk_calc = chunk_size / pool_size * 100
            if (chunk_size % 1 == 0) and (chunk_calc <= 5 and chunk_calc >= 2):
                return int(instances), int(chunk_size)
        return 1, pool_size # Defaults to a single pool at the maximum pool size

    def config_check(file):
        return exists(file)

    def config_read(lines):
        for line in lines:
            print(line)

    def config_save(new_config, file):
        with open(file, 'w') as stream:
            for line in new_config:
                stream.write(f'{line}\n')
        mysql_restart()

    def config_update(file, **config):
        if not config_check(file):
            print(f'File {file} does not exist')
            _exit(1)
        with open(file, 'r') as stream:
            file_lines = [x.strip('\n') for x in stream.readlines()]
        if '[mysqld]' not in file_lines:
            file_lines.append('[mysqld]')
        for key, value in config.items():
            for line in file_lines:
                if line.find(key) >= 0:
                    file_lines.remove(line)
            file_lines.append(f'{key} = {value}')
        return file_lines

    def config_commit(file, new_config):
        while True:
            resp = input(
                'Configuration ready. Commit now?\n [y] Yes  [n] No  [r] Read Config : ')
            if resp[0].lower() == 'y':
                config_save(new_config, file)
            elif resp[0].lower() == 'n':
                print('Commit declined. Exiting...')
                _exit(1)
            elif resp[0].lower() == 'r':
                config_read(new_config)

    def mysql_restart():
        while True:
            resp = input('Configuration has been applied. Restart MySQL now?\n[y] Yes  [n] No  [s] Schedule : ')
            if resp[0].lower() == 'y':
                system('service mysql restart')
                _exit(0)
            elif resp[0].lower() == 'n':
                print('MySQL reboot declined. You will need to restart the service for changes to take effect.')
                _exit(0)
            elif resp[0].lower() == 's':
                time = input('Enter time to restart MySQL\n(e.g. tomorrow 10am, now + 30 minutes, etc) : ')
                if check_output(f'echo "service mysql restart" | at {time}', shell=True) == 1:
                    print(f'Failed to schedule ')
                    _exit(1)
                _exit(0)
    
    mem_kb = dict((i.split()[0].rstrip(':'),int(i.split()[1])) for i in open('/proc/meminfo').readlines())['MemTotal']
    if memory and memory <= mem_kb:
        mem_kb = memory
    
    data = {}
    data['innodb_buffer_pool_size'] = calc_pool_size(mem_kb, percent)
    data['innodb_buffer_pool_instances '], data['innodb_buffer_pool_chunk_size '] = calc_pool_dependents(data['innodb_buffer_pool_size'])
    new_config = config_update(file, **data)

    if not commit:
        return config_read(new_config)
    config_commit(file, new_config)


if __name__ == '__main__':
    app = fire.Fire(main)
    
    