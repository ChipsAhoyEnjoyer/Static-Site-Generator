#!/bin/bash
python3 -m unittest discover -s src > output.log 2>&1
cat output.log