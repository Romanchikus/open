reset:
	rm scripts/db.sqlite3 -f
	find opencourse/courses/migrations/ -name '00*.py' -delete
	find opencourse/profiles/migrations/ -name '00*.py' -delete
	pip install -r requirements/local.txt
	./manage.py makemigrations
	./manage.py migrate
	./manage.py runscript 2020_05_10_2
	./manage.py runscript 2020_05_11

translate:
	./manage.py makemessages -i venv -i */account
	./manage.py compilemessages -i venv -l fr

dumpdb:
	./manage.py dumpscript courses profiles account.EmailAddress > scripts/db_dump.py
