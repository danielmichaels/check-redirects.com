# Flask Blueprint

> A starter template based upon [Nick Janetakis](buildasaasappwithflask.com)' 
> course

## TODO

- [ ] Clean out "snakeeyes" icons and references
- [ ] Clean out `assets/app/modules`

## Features

- [x] Flask
- [x] Celery
- [x] Docker (docker-compose)
- [x] User Registration
- [x] Flask-Mail Intergration

## Setup

1. Copy `.env.example` to `.env` && copy `*.override.example.yml` to `*.override.yml`. 
Else, `webpack` won't build.

2. Add your email credentials to your `.env` file.

3. Open a terminal configured to run Docker and then run:

```shell script
docker-compose down -v # -v removes volumes
docker-compose build --no-cache # start fresh
docker-compose up 
docker-compose exec web flask db reset --with-testdb # must do
docker-compose exec web flask babel

# The following are helper scripts but not needed to start the app
docker-compose exec web flask add all
docker-compose exec web flask flake8
docker-compose exec web flask test
docker-compose exec web flask cov
docker-compose exec web flask loc
docker-compose exec web flask secret
#docker-compose exec web flask stripe sync-plans # no longer needed but kept for reference
```

