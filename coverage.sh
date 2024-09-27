poetry shell
coverage run --omit "tests/*" -m pytest ./tests/ --junitxml=./report.xml -s
genbadge tests -i ./report.xml -s -o ./badges/tests.svg
genbadge coverage -i ./coverage.xml -s -o ./badges/coverage.svg
coverage report