#!/usr/bin/python3

from subprocess import Popen
import sys

filename = ("controlscript.py")
while True:
    print("\nStarting " + filename)
    p = Popen("python3 " + filename, shell=True)
    p.wait()
