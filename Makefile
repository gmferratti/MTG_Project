# Makefile
create-env:
    python -m venv venv
    venv/Scripts/python -m pip install --upgrade pip
    venv/Scripts/python -m pip install -r mtg-project/src/mtg_project/requirements.txt

run:
    cmd /c "cd mtg-project && ..\\venv\\Scripts\\python -m kedro run"

clean:
    cmd /c "if exist __pycache__ rmdir /s /q __pycache__"
    cmd /c "if exist .pytest_cache rmdir /s /q .pytest_cache"
    cmd /c "for /R %i in (*.pyc) do del /f /q \"%i\""

lint-all:
    cmd /c "cd mtg-project && ..\\venv\\Scripts\\python -m black . && ..\\venv\\Scripts\\python -m flake8 && ..\\venv\\Scripts\\python -m isort ."

# Obs. I am using pymake instead of make
