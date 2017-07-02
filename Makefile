req:
	pip3 install --upgrade -r requirements.txt -t lib

deploy:
	git push heroku heroku:master
