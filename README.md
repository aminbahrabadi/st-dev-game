# Simple Question Game
## Live demo
You can test live demo here: [Simple Question Game](https://st-dev.pytsts.ir)
### Users:
<br />Admin:
<br />username: game_admin
<br />password: bkfijSWqz44YDV2
## How to run
- Create a Postgresql database
- Clone the project
- Update .env file based on your credentials
- Open terminal and create a virtual environment:
```sh
virtualenv venv
```
- Activate virtual environment:
```sh
source venv/bin/activate
```
- Install packages:
```sh
pip install -r requirements.txt
```
- Migrate and create database:
```sh
python manage.py migrate
```
- Run server:
```sh
python manage.py runserver
```
- Open the browser and browse this URL:
```sh
127.0.0.1:8000
```
### Manage Questions:
<br />URL: ```/question/list/```
<br />You can add Questions and Answers here. Only a user with the role of Admin can manage questions.

