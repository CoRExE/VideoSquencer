@echo off

echo "If the next command line crash, check your Python Installation"

timeout 3

python -V

timeout 5

pip install -U opencv-python
pip install -U Jinja2
pip install -U numpy

echo "Requirement Installed"

timeout 3

copy Run.bat ..\Run.bat
