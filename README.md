# Create User tests
Foram feitas alterações à tabela excell do "Testes Create User"

## Tests
It will run exactly 64 tests for each column of the decision table.
All tests should pass, but only 2 will actually create a new user (or simulate if user already exists) - TC2. The other 62 are for the failing scenarios - TC1

## Install
1. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```
2. Upgrade pip
```bash
pip install --upgrade pip
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers
```bash
playwright install
```


## How to run
From the root dir, run:
```bash
PYTHONPATH=. pytest -n auto -v
```

This will run all the tests in parallel

To show the tests executing (Browser UI) go to ``conftest.py`` in line 10, change to ``headless=False,``, and run with:
```bash
PYTHONPATH=. pytest -v
```

