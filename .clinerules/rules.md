# Cline Rules

## Always Use Python Virtual Environment

This project uses a Python virtual environment located at `venv/`. **Always** use the virtual environment when running any Python-related commands.

### How to use the virtual environment

Because each shell command runs in a new session, `source venv/bin/activate` does **not** persist between commands. Instead, use one of these two approaches:

**Option 1 (preferred): Use the venv binaries directly**
```bash
venv/bin/python main.py ...
venv/bin/pip install ...
venv/bin/pytest ...
```

**Option 2: Chain activation with the command in a single call**
```bash
source venv/bin/activate && python main.py ...
source venv/bin/activate && pip install ...
source venv/bin/activate && pytest ...
```

### Setup (if venv does not exist)
```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

This ensures dependencies are managed correctly and avoids system-wide installations.
