install:
	python3 -m pip install --upgrade pip &&\
		python3 -m pip install -r ./config/requirements.txt
		
sudo_install_redoc-cli:
	sudo apt-get update &&\
		sudo apt install npm &&\
		sudo npm install -g redoc-cli


lint:
	find . -type f -name "*.py" | xargs pylint 

flake8:
	flake8 --format=html --htmldir='static/reports/' --statistics &&\
		mv static/reports/index.html static/reports/flake8_report.html

bandit:
	bandit -r . --configfile ./config/bandit.yaml -f html -o static/reports/bandit_report.html -v

test:
	python3 -m pytest -vv --disable-pytest-warnings --html='./static/reports/pytest_report.html' --self-contained-html

document:
	redoc-cli bundle ./config/openapi.yaml &&\
		mv redoc-static.html static/documents/api-document.html

check:
	flake8
	flake8 --format=html --htmldir='static/reports/' --statistics
	mv static/reports/index.html static/reports/flake8_report.html
	find . -type f -name "*.py" | xargs pylint 
	bandit -r . --configfile ./config/bandit.yaml
	python3 -m pytest -vv --disable-pytest-warnings --html='./static/reports/pytest_report.html' --self-contained-html
	redoc-cli bundle ./config/openapi.yaml
	mv redoc-static.html static/documents/api-document.html

# all: lint flake8 bandit