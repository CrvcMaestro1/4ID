4ID Challenge
=====================================================================

Docker setup
=======================

### Run docker compose

```bash
$ docker-compose -f docker-compose.yml up
```

### Open API Docs

http://localhost:5000/docs

### Adminer DB Viewer

http://localhost:8080/?pgsql=db&username=postgres&db=challenge_4id_docker&ns=auth

### Logging

You can see the logs in console below

### Down docker compose

```bash
$ docker-compose down --rmi all
```