#!/bin/sh

bash clean_repo.sh

python3 -m venv ~/sgoinfre/local_lib
bash source ~/sgoinfre/local_lib/bin/activate

pip3 --version

sleep 3

pip3 install --log path.log --upgrade --force-reinstall  git+https://github.com/jaraco/path.py.git

cp my_program.py ~/sgoinfre/
python3 ~/sgoinfre/my_program.py
