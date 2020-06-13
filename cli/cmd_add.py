import random
from datetime import datetime

import click
from faker import Faker
from flask import current_app
from flask.cli import with_appcontext

from app.extensions import db

fake = Faker()


def _log_status(count, model_label):
    """
    Log the output of how many records were created.

    :param count: Amount created
    :type count: int
    :param model_label: Name of the model
    :type model_label: str
    :return: None
    """
    click.echo("Created {0} {1}".format(count, model_label))


@with_appcontext
def _bulk_insert(model, data, label):
    """
    Bulk insert data to a specific model and log it. This is much more
    efficient than adding 1 row at a time in a loop.

    :param model: Model being affected
    :type model: SQLAlchemy
    :param data: Data to be saved
    :type data: list
    :param label: Label for the output
    :type label: str
    :param skip_delete: Optionally delete previous records
    :type skip_delete: bool
    :return: None
    """
    model.query.delete()

    db.session.commit()
    db.engine.execute(model.__table__.insert(), data)

    _log_status(model.query.count(), label)


@click.group()
def add():
    """ Add items to the database. """
    pass


@add.command()
@with_appcontext
def users():
    """
    Generate fake users.
    """
    app_config = current_app.config

    random_emails = []
    data = []

    click.echo("Working...")

    # Ensure we get about 100 unique random emails.
    for i in range(0, 99):
        random_emails.append(fake.email())

    random_emails.append(app_config["SEED_ADMIN_EMAIL"])
    random_emails = list(set(random_emails))

    while True:
        if len(random_emails) == 0:
            break

        fake_datetime = fake.date_time_between(
            start_date="-1y", end_date="now"
        ).strftime("%s")

        created_on = datetime.utcfromtimestamp(float(fake_datetime)).strftime(
            "%Y-%m-%dT%H:%M:%S Z"
        )

        random_percent = random.random()

        if random_percent >= 0.05:
            role = "member"
        else:
            role = "admin"

        email = random_emails.pop()

        random_percent = random.random()

        if random_percent >= 0.5:
            random_trail = str(int(round((random.random() * 1000))))
            username = fake.first_name() + random_trail
            last_bet_on = created_on
        else:
            username = None
            last_bet_on = None

        fake_datetime = fake.date_time_between(
            start_date="-1y", end_date="now"
        ).strftime("%s")

        current_sign_in_on = datetime.utcfromtimestamp(
            float(fake_datetime)).strftime(
            "%Y-%m-%dT%H:%M:%S Z"
        )

        params = {
            "created_on": created_on,
            "updated_on": created_on,
            "role": role,
            "email": email,
            "username": username,
            # 'password': User.encrypt_password('password'),
            "sign_in_count": random.random() * 100,
            "coins": 100,
            "last_bet_on": last_bet_on,
            "current_sign_in_on": current_sign_in_on,
            "current_sign_in_ip": fake.ipv4(),
            "last_sign_in_on": current_sign_in_on,
            "last_sign_in_ip": fake.ipv4(),
        }

        # Ensure the seeded admin is always an admin with the seeded password.
        # if email == app_config['SEED_ADMIN_EMAIL']:
        #     password = User.encrypt_password(app_config['SEED_ADMIN_PASSWORD'])

        # params['role'] = 'admin'
        # params['password'] = password

        # data.append(params)

    # return _bulk_insert(User, data, 'users')


@add.command()
@click.pass_context
@with_appcontext
def all(ctx):
    """
    Generate all data.

    :param ctx:
    :return: None
    """
    ctx.invoke(users)
