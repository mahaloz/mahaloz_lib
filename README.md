# mahaloz_lib
A Python library for my often reused CTF scripts, packages, and configs (including dotfiles).

## Installation
```bash
pip install -e .
```
If you are using it for a first system setup, then do
```bash
pip install -e .[system_setup]
```

## Usage
### Setting up a mahaloz System
```bash
python3 -m mahaloz_lib --setup-system
```
Use the `--no-packages` to only install config files (which may install other packages).