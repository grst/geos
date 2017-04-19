req:
	pip3 install --upgrade -r requirements.txt -t lib

deploy:
	gcloud app deploy
