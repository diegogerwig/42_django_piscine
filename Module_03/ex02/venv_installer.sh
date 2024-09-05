bash clean_repo.sh

python3 -m venv ~/sgoinfre/django
bassh source ~/sgoinfre/django/bin/activate

pip install -r requirement.txt

pip freeze > requirement.txt