#!/bin/sh

/usr/bin/python3 -m venv django_venv
source django_venv/bin/activate

#python3 -m pip install Django
#python3 -m pip freeze > requirement.txt
python3 -m pip install -r requirement.txt
#python3 -m pip list
