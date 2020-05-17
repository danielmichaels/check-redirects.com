-----------------------------------
Getting everything up and running
-----------------------------------

1. Copy .env.example to .env && copy *.override.example.yml to *.override.yml

2. Add your email and Stripe credentials to your .env file.
  (use your instance/settings.py file from section 20's code as a reference)

3. Open a terminal configured to run Docker and then run:

docker-compose down -v
docker-compose build --no-cache
docker-compose up
docker-compose exec web flask db reset --with-testdb
docker-compose exec web flask stripe sync-plans
docker-compose exec web flask babel
docker-compose exec web flask add all
docker-compose exec web flask flake8
docker-compose exec web flask test
docker-compose exec web flask cov
docker-compose exec web flask loc
docker-compose exec web flask secret
