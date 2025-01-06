set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

python manage.py loaddata data/fixtures/region.json
python manage.py loaddata data/fixtures/gender.json
python manage.py loaddata data/fixtures/results.json
