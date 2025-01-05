set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

# Transfer old data from SQLite to PostgreSQL
# Check if the data.json file exists
if [ -f "regions.json" ]; then
    echo "Loading data from data.json into the database..."
    python manage.py loaddata data.json
else
    echo "No data.json file found. Skipping data import."
fi