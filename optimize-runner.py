#!/usr/bin/python3

from .bootstrap.optimize import main
import fire

if __name__ == '__main__':
    app = fire.Fire(main)