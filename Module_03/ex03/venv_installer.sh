bash clean_repo.sh

python3 -m venv ~/sgoinfre/django
source ~/sgoinfre/django/bin/activate

if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo '✅ Virtual environment activated.'
else
    echo '❌ Failed to activate virtual environment.'
fi

pip install -r requirement.txt
