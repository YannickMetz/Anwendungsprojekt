#! /bin/bash
python3 -m pytest tests_pytest/ --cov-report html --cov-report xml:cov.xml  --cov=app

# HTML files in "htmlcov/" lassen sich mit "Live Preview" VS Code Extension anzeigen (Rechtsclick)
# cov.xml wird verwendet von "Coverage Gutters" VS Code Extension für Preview im Quelltext 