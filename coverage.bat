#!/usr/bin/env sh
python -m coverage run --omit "tests/*.py" -m pytest ./tests/ --junitxml=./report.xml -s
python -m coverage xml
genbadge tests -i ./report.xml -s -o ./badges/tests.svg
genbadge coverage -i ./coverage.xml -s -o ./badges/coverage.svg
