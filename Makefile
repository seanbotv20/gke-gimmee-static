build: freeze
	docker build . -t seanbot/gke-gimmee-static

deploy:
	docker push seanbot/gke-gimmee-static

freeze: requirements.txt
	pipenv run pip freeze > requirements.txt