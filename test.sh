while ! mysqladmin ping -h mysql -uroot --silent; do
    sleep 1
done
mysql -h mysql -uroot test < db/db.sql
mysql -h mysql -uroot test < db/test.sql
python3 create_admin.py admin
pytest --ruff app --cov=app tests
