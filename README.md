# Simple Question Game
## Live demo
You can test live demo here: [Simple Question Game](https://st-dev-game.ir)
### Users:
<br />Admin:
username: admin_user
password: zewsM5UwbMNaBFc
## How to run
1. Clone the project
2. Open terminal and create a virtual environment:
<br />```virtualenv venv```
3. Activate virtual environment:
<br />```source venv/bin/activate```
4. Install packages:
<br />```pip install -r requirements.txt```
5. Migrate and create database:
<br />```python manage.py migrate```
6. Run server:
<br />```python manage.py runserver```
7. Open the browser and browse this URL:
<br />```127.0.0.1:8000```
### Manage Questions:
<br />URL: ```/question/list/```
You can add Questions and Answers here. Only a user with the role of Admin can manage questions.

