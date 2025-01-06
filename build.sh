set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

python manage.py loaddata data_diabetesdata.json
python manage.py loaddata data_gender.json
python manage.py loaddata data_region.json
python manage.py loaddata data_results.json
