# FastAPI-Skeleton
[![Build Status](https://github.com/keakon/fastapi-skeleton/actions/workflows/python.yml/badge.svg)](https://github.com/keakon/fastapi-skeleton/actions)
[![Coverage](https://codecov.io/gh/keakon/fastapi-skeleton/branch/master/graph/badge.svg)](https://codecov.io/gh/keakon/fastapi-skeleton)

FastAPI-Skeleton is a web application template of FastAPI with best practice.

## Requirements

1. Python 3.10 or later, tested on the latest CPython version.
2. Redis.
3. MySQL 8.0 or later.

## Prepare database

```bash
$ redis-server &
$ sudo systemctl start mysql  # or "brew services run mysql" in macOS
$ mysql -u root -e "CREATE DATABASE IF NOT EXISTS test"
$ mysql -u root test < db/db.sql
```

## Run locally

```bash
$ pip install -r requirements.txt
$ python create_admin.py admin  # or change "admin" to your password
$ uvicorn app.main:app 
```

## Test

```bash
$ mysql -u root test < db/test.sql
$ pip install -r requirements-test.txt
$ pytest --ruff app --cov=app tests
$ coverage html
```

## Build and run with docker

```bash
$ docker-compose build
$ docker-compose up -d
```

## Try api docs.

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
