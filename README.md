# Survey

Survey is a REST-based service with the API keys access. 
Responses will be in JSON format

In English below
##### Задание: 
 спроектировать и разработать API для системы опросов пользователей.

###### Функционал для администратора системы:

- авторизация в системе (регистрация не нужна)
- добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта, дата окончания, описание. После создания поле "дата старта" у опроса менять нельзя
- добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)

###### Функционал для пользователей системы:

- получение списка активных опросов
- прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя

Использовать следующие технологии: Django 3.1.6, Django REST framework.

Результат выполнения задачи:
- исходный код приложения в github (только на github, публичный репозиторий)
- инструкция по разворачиванию приложения (в docker или локально)
- документация по API

##### Task:
To design and develop an API for a user polling system.

###### Working options for system admistrator:
* system authorization (registration is not required).
* adding / changing / deleting polls. Poll attributes: title, start date, end date, description. Once it created then the field “start date” for the survey cannot be changed.
* adding / changing / deleting questions in the survey. Question attributes: question text, question type (text answer, single option reply, multiple option reply).

###### Working options for users of the service:
* obtaining a list of current polls.
* taking a poll: polls can be completed anonymously, a numeric ID is passed into API as a user identifier, by which the user's replies to questions are stored; one user can participate in any number of surveys.
* retrieving polls completed by a user with details by the answers (what is selected) by unique user ID.

Required specifications: Django 3.1.6, Django REST framework.

Task outcomes:
* application source code uploaded on github (public repository)
* instructions for deploying the application (docker or locally)
* API documentation



### Quick Start Guide
#### Installation
System-wide dependencies:
-Python 3.8
-Django 3.1.6
-djangorestframework



Clone git repository:
```sh
https://github.com/statcio/questionnarie.git
```
Launch docker CLI command:
```sh
docker-compose build
```
Create database migrations:
```sh
docker-compose run api python manage.py makemigrations
docker-compose run api python manage.py migrate
```
Create superuser:
```sh
docker-compose run api python manage.py createsuperuser 
```
Fill required data:
```sh
Username (leave blank to use ...): 
Email address: 
Password: 
Password (again): 
Superuser created successfully. 
```

Run application (by default: http://0.0.0.0:8000/):
```sh
docker-compose up
```


## API Documentation

##### User Authorization:
* Request method: GET
* URL: http://0.0.0.0:8000/api/login/
* Body:
     -  username:
     -  password:
* sample CLI command:
```sh
curl --location --request GET 'http://0.0.0.0:8000/api/login/' \
--form 'username=... ' \
--form 'password=...'
```

##### To create a poll:
* Request method: POST
* URL: http://0.0.0.0:8000/api/polls/create/
* Header:Authorization: Token userToken
* Body:
     - title: title
     - start_date:  start date, format: YYYY-MM-DDTHH:MM:SS
     - end_date: end date, format: YYYY-MM-DDTHH:MM:SS
     - description: description
* sample CLI command:
```sh
curl --location --request POST 'http://0.0.0.0:8000/api/polls/create/' \
--header 'Authorization: Token %userToken' \
--form 'title=...' \
--form 'start_date=...' \
--form 'end_date=...' \
--form 'description=...'
```

##### To update a poll:
* Request method: PATCH
* URL: http://0.0.0.0:8000/api/polls/update/[poll_id]/
* Header: Authorization: Token userToken
* Param: poll_id
* Body:
     - title: title
     - end_date: poll end date, format: YYYY-MM-DDTHH:MM:SS
     - description: description 
* sample CLI command:
```sh
curl --location --request PATCH 'http://0.0.0.0:8000/api/polls/update/[poll_id]/' \
--header 'Authorization: Token %userToken' \
--form 'title=...' \
--form 'end_date=... \
--form 'description=...'
```

##### To delete a poll:
* Request method: DELETE
* URL: http://0.0.0.0:8000/api/polls/update/[poll_id]
* Header: Authorization: Token userToken
* Param: poll_id 
* sample CLI command:
```sh
curl --location --request DELETE 'http://0.0.0.0:8000/api/polls/update/[poll_id]/' \
--header 'Authorization: Token %userToken'
```

##### To review all polls:
* Request method: GET
* URL: http://0.0.0.0:8000/api/polls/view/
* Header: Authorization: Token userToken
* sample CLI command:
```sh
curl --location --request GET 'http://0.0.0.0:8000/api/polls/view/' \
--header 'Authorization: Token %userToken'
```

##### To review the current polls:
* Request method: GET
* URL: http://0.0.0.0:8000/api/polls/view/active/
* Header: Authorization: Token userToken
* sample CLI command:
```sh
curl --location --request GET 'http://0.0.0.0:8000/api/polls/view/active/' \
--header 'Authorization: Token %userToken'
```

##### To create a question:
* Request method: POST
* URL: http://0.0.0.0:8000/api/question/create/
* Header: Authorization: Token userToken
* Body:
     - poll: id 
     - question_text: text
     - question_type: OPTION, MULTIOPTION or TEXT
* sample CLI command:
```sh
curl --location --request POST 'http://0.0.0.0:8000/api/question/create/' \
--header 'Authorization: Token %userToken' \
--form 'poll=...' \
--form 'question_text=...' \
--form 'question_type=...' \
```

##### To update a question:
* Request method: PATCH
* URL: http://0.0.0.0:8000/api/question/update/[question_id]/
* Header: Authorization: Token userToken
* Param: question_id
* Body:
     - poll: id 
     - question_text: question
     - question_type: OPTION, MULTIOPTION or TEXT
* sample CLI command:
```sh
curl --location --request PATCH 'http://0.0.0.0:8000/api/question/update/[question_id]/' \
--header 'Authorization: Token %userToken' \
--form 'poll=...' \
--form 'question_text=...' \
--form 'question_type=...' \
```

##### To delete a question:
* Request method: DELETE
* URL: http://0.0.0.0:8000/api/question/update/[question_id]/
* Header: Authorization: Token userToken
* Param: question_id
* sample CLI command:
```sh
curl --location --request DELETE 'http://0.0.0.0:8000/api/question/update/[question_id]/' \
--header 'Authorization: Token %userToken' \
--form 'poll=...' \
--form 'question_text=...' \
--form 'question_type=...' \
```

##### To create an option:
* Request method: POST
* URL: http://0.0.0.0:8000/api/option/create/
* Header: Authorization: Token userToken
* Body:
     - question: id 
     - option_text: text
* sample CLI command:
```sh
curl --location --request POST 'http://0.0.0.0:8000/api/option/create/' \
--header 'Authorization: Token %userToken' \
--form 'question=...' \
--form 'option_text=...'
```

##### To update an option:
* Request method: PATCH
* URL: http://0.0.0.0:8000/api/option/update/[option_id]/
* Header: Authorization: Token userToken
* Param: option_id
* Body:
     - question: id 
     - option_text: text
* sample CLI command:
```sh
curl --location --request PATCH 'http://0.0.0.0:8000/api/option/update/[option_id]/' \
--header 'Authorization: Token %userToken' \
--form 'question=...' \
--form 'option_text=...'\
```

##### To delete an option:
* Request method: DELETE
* URL: http://0.0.0.0:8000/api/option/update/[option_id]/
* Header: Authorization: Token userToken
* Param:option_id
* sample CLI command:
```sh
curl --location --request DELETE 'http://0.0.0.0:8000/api/option/update/[option_id]/' \
--header 'Authorization: Token %userToken' \
--form 'question=...' \
--form 'option_text=...'
```

##### To create a reply:
* Request method: POST
* URL: http://0.0.0.0:8000/api/reply/create/
* Header:Authorization: Token userToken
* Body:
     - poll: id 
     - question: id 
     - option_text: text
     - option: id or "" by default
* sample CLI command:
```sh
curl --location --request POST 'http://0.0.0.0:8000/api/reply/create/' \
--header 'Authorization: Token %userToken' \
--form 'poll=...' \
--form 'question=...' \
--form 'option=...' \
--form 'option_text=...'\
```

##### To update a reply:
* Request method: PATCH
* URL: http://0.0.0.0:8000/api/reply/update/[reply_id]/
* Header:Authorization: Token userToken
* Param:reply_id
* Body:
     - poll: id 
     - question: id of question
     - option_text: text
     - option: id or "" by default
* sample CLI command:
```sh
curl --location --request PATCH 'http://0.0.0.0:8000/api/reply/update/[reply_id]' \
--header 'Authorization: Token %userToken' \
--form 'poll=...' \
--form 'question=%question' \
--form 'option=... \
--form 'option_text=...'\
```

##### To delete a reply:
* Request method: DELETE
* URL: http://0.0.0.0:8000/api/reply/update/[reply_id]/
* Header: Authorization: Token userToken
* Param: reply_id
* sample CLI command:
```sh
curl --location --request DELETE 'http://0.0.0.0:8000/api/reply/update/[reply_id]' \
--header 'Authorization: Token %userToken'
```

##### To review all the user replies:
* Request method: GET
* URL: http://0.0.0.0:8000/api/reply/view/[user_id]/
* Param: user_id
* Header: Authorization: Token userToken
* sample CLI command:
```sh
curl --location --request GET 'http://0.0.0.0:8000/api/reply/view/[user_id]' \
--header 'Authorization: Token %userToken'
```








