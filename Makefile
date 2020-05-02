setup:
	./scripts/bootstrap.sh

update_requirements:
	poetry export -f requirements.txt -o requirements.txt

deploy:
	git push heroku master
