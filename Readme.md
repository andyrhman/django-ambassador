# Django Auth

<p align="center">
  <img src="https://1000logos.net/wp-content/uploads/2020/08/Django-Logo.png" width="300" height="200" />
</p>

## Introduction

This is my 2nd project of django web framework, no that i know mostly on how this django structure api works and in this project i want to sharpen my skill again to study more on how this api works with admin api project.

## First Time Set Up & Configuration

Install the Django Web Framework:

```bash
pip install django
pip install djangorestframework   
pip install django-filter   
pip install psycopg2 # For database
pip install python-decouple # Installing python-decouple for .env:
```

Create the directory:

```bash
mkdir django-auth
django-admin startproject app .
django-admin startapp <folder name>

```

## Adding first migration

Before you use docker create the app and the model
```bash
django-admin startapp <folder name>
python3 manage.py makemigrations
python manage.py migrate
python3 manage.py runserver
python manage.py createsuperuser --email test3@mail.com
```

Go To settings.py and add this:

```python
INSTALLED_APPS = [
  // other lists,
  "rest_framework",
  "core"
]
```

## Features

List the main features of your autth server. For example:
- User authentication and authorization
- Auth Token
- 2FA Authentication

## Installation

Provide step-by-step instructions for installing and setting up the project locally. Include commands and any additional configurations. For example:

```bash
git clone https://github.com/andyrhman/django-ambassador.git
cd django-ambassador
pip install -r requirements.txt