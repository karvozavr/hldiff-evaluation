#!/usr/bin/env python3
import os

import click


@click.command()
@click.argument('directory')
def generate(directory):
    for root, d, f in os.walk(directory, topdown=True):
        for name in f:
            print(name)


if __name__ == '__main__':
    generate()
