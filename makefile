.PHONY: api ui

api:
	cd api; python manage.py runserver -r

ui:
	cd ui; python -m SimpleHTTPServer
