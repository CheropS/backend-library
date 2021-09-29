"""Manage file"""
from flask import render_template
from flask_migrate import Migrate

from api import db, app
from api import routes
from api.models import User

app.register_blueprint(routes.mod)

migrate = Migrate(app, db)


# Route to Index Page
@app.route('/')
def index():
    """Route to Index Page"""
    return render_template('documentation.html')


@app.cli.command("db")
def db():
    """command to migrate"""


@app.cli.command("create_admin")
def create_admin():
    """Create admin function"""
    email = input('Enter email: ')
    username = input('Enter username: ')
    first_name = input('Enter first name: ')
    last_name = input('Enter last name: ')
    password = input('Enter password: ')
    try:
        admin = User(email, username, first_name, last_name, password)
        admin.is_admin = True
        admin.save()
    except Exception as e:
        print(e)
    print('Admin user created successfully')


@app.cli.command("tests")
def test():
    """
    function to run tests
    :return: tests passed
    """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    app.run()
