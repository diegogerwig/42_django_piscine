#!/bin/sh

python3 -m venv ~/sgoinfre/local_lib
source ~/sgoinfre/local_lib/bin/activate

pip3 --version

sleep 5



pip3 install --log path_py_module_install.log --upgrade --force-reinstall  git+https://github.com/jaraco/path.py.git

cp my_program.py ~/sgoinfre/
python3 ~/sgoinfre/my_program.py
