reset:
	rm scripts/db.sqlite3 -f
	pip install -r requirements/local.txt

	find opencourse/courses/migrations/ -name '00*.py' -delete
	find opencourse/profiles/migrations/ -name '00*.py' -delete
	./manage.py makemigrations
	./manage.py migrate
	./manage.py runscript auth_data
	./manage.py runscript opencourse_data

trans:
	./manage.py makemessages -i venv -i */account
	./manage.py compilemessages -i venv -l fr

dumpdb:
	./manage.py dumpscript courses profiles account.EmailAddress > scripts/db_dump.py

deploy:
	git fetch origin
	git reset origin/master --hard

	pip install -r requirements/production.txt
	./manage.py compilemessages -i venv
	./manage.py collectstatic --noinput
	./manage.py migrate

	systemctl restart nginx gunicorn.socket gunicorn.service gunicorn

migr:
	./manage.py makemigrations
	./manage.py migrate

blankdb:
	rm db.sqlite3 -f
	./manage.py makemigrations
	./manage.py migrate
	./manage.py runscript help_data

testdb:
	rm db.sqlite3 -f
	./manage.py makemigrations
	./manage.py migrate
	./manage.py runscript help_data
	./manage.py runscript opencourse_data