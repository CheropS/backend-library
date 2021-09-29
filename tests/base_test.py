from api import app, db
from config import app_config
from api.models import User

import unittest
from flask import json


class TestHelloBooks(unittest.TestCase):
    """Hello Books Test Base Class"""

    def setUp(self):
        """Set up function before any test runs"""
        self.app = app
        self.version = '/api/v1'
        app.config.from_object(app_config['testing'])
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Registration Test Data
        self.user_data = {
            "email":"zootest@yahoo.com",
            "username":"zootest",
            "first_name":"Zootest",
            "last_name":"Gang",
            "password":"password1234",
            "confirm_password":"password1234"
        }
        self.user_data2 = {
            "email":"zootest@yahoo.com",
            "username":"zootest",
            "first_name":"Zootest",
            "last_name":"Gang",
            "password":"password1234",
            "confirm_password":"password1234"
        }
        self.empty_user_data = {

        }
        self.user_data_no_email = {
            "email":"",
            "username":"zootest",
            "first_name":"Zootest",
            "last_name":"Gang",
            "password":"password1234",
            "confirm_password":"password1234"
        }
        self.user_data_wrong_email = {
            "email":"hgtfd",
            "username":"zootest",
            "first_name":"Zootest",
            "last_name":"Gang",
            "password":"password1234",
            "confirm_password":"password1234"
        }
        self.user_data_long_email = {
            "email":"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn@gmail.com",
            "username":"zootest",
            "first_name":"Zootest",
            "last_name":"Gang",
            "password":"password1234",
            "confirm_password":"password1234"
        }
        self.user_data_no_username = {
            "email":"zootest@yahoo.com",
            "username":"",
            "first_name":"Zootest",
            "last_name":"Gang",
            "password":"password1234",
            "confirm_password":"password1234"
        }
        self.user_data_long_username = {
            "email":"zootest@yahoo.com",
            "username":"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn",
            "first_name":"Zootest",
            "last_name":"Gang",
            "password":"password1234",
            "confirm_password":"password1234"
        }
        self.user_data_no_first_name = {
            "email":"zootest@yahoo.com",
            "username":"zootest",
            "first_name":"",
            "last_name":"Gang",
            "password":"password1234",
            "confirm_password":"password1234"
        }
        self.user_data_long_first_name = {
            "email":"zootest@yahoo.com",
            "username":"zootest",
            "first_name":"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn",
            "last_name":"Gang",
            "password":"password1234",
            "confirm_password":"password1234"
        }
        self.user_data_no_last_name = {
            "email":"zootest@yahoo.com",
            "username":"zootest",
            "first_name":"Zootest",
            "last_name":"",
            "password":"password1234",
            "confirm_password":"password1234"
        }
        self.user_data_long_last_name = {
            "email":"zootest@yahoo.com",
            "username":"zootest",
            "first_name":"Zootest",
            "last_name":"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn",
            "password":"password1234",
            "confirm_password":"password1234"
        }
        self.user_data_no_password = {
            "email":"zootest@yahoo.com",
            "username":"zootest",
            "first_name":"Zootest",
            "last_name":"Gang",
            "password":"",
            "confirm_password":""
        }
        self.user_data_short_password = {
            "email":"zootest@yahoo.com",
            "username":"zootest",
            "first_name":"Zootest",
            "last_name":"Gang",
            "password":"pass",
            "confirm_password":"pass"
        }
        self.user_data_no_confirm = {
            "email":"zootest@yahoo.com",
            "username":"zootest",
            "first_name":"Zootest",
            "last_name":"Gang",
            "password":"password1234",
            "confirm_password":""
        }
        self.user_data_password_mismatch = {
            "email":"zootest@yahoo.com",
            "username":"zootest",
            "first_name":"Zootest",
            "last_name":"Gang",
            "password":"password1234",
            "confirm_password":"pass"
        }

        #Login Test Data
        self.login_data = {
            "username": "zootest",
            "password": "password1234"
        }
        self.login_data_user_not_exist = {
            "username": "harry",
            "password": "password1234"
        }
        self.login_data_password_mismatch = {
            "username": "zootest",
            "password": "password123"
        }
        self.book_data = {
            "title":"Windmills of Gods",
            "author":"Sidney Sheldon",
            "isbn":"3652472876",
            "publisher": "Publisher",
            "quantity": 45
        }
        self.empty_book_data = {

        }
        self.book_data_no_title = {
            "title":"",
            "author":"Sidney Sheldon",
            "isbn":"3652472876",
            "publisher": "Publisher",
            "quantity": 45
        }
        self.book_data_no_author = {
            "title":"Windmills of Gods",
            "author":"",
            "isbn":"3652472876",
            "publisher": "Publisher",
            "quantity": 45
        }
        self.book_data_no_isbn = {
            "title":"Windmills of Gods",
            "author":"Sidney Sheldon",
            "isbn":"",
            "publisher": "Publisher",
            "quantity": 45
        }
        self.book_data_no_publisher = {
            "title":"Windmills of Gods",
            "author":"Sidney Sheldon",
            "isbn":"3652472876",
            "publisher": "",
            "quantity": 45
        }
        self.book_data_no_quantity = {
            "title":"Windmills of Gods",
            "author":"Sidney Sheldon",
            "isbn":"3652472876",
            "publisher": "Publisher",
            "quantity": None
        }
        self.update_book_data = {
            "title":"Windmills of Gods",
            "author":"Sidney Sheldon",
            "isbn":"3652472876",
            "publisher": "Publisher",
            "quantity": 100
        }
        self.update_book_data_empty = {

        }
        self.update_book_data_no_title = {
            "title":"",
            "author":"Sidney Sheldon",
            "isbn":"3652472876",
            "publisher": "Publisher",
            "quantity": 100
        }
        self.update_book_data_no_author = {
            "title":"Windmills of Gods",
            "author":"",
            "isbn":"3652472876",
            "publisher": "Publisher",
            "quantity": 100
        }
        self.update_book_data_no_isbn = {
            "title":"Windmills of Gods",
            "author":"Sidney Sheldon",
            "isbn":"",
            "publisher": "Publisher",
            "quantity": 100
        }
        self.update_book_data_no_publisher = {
            "title":"Windmills of Gods",
            "author":"Sidney Sheldon",
            "isbn":"3652472876",
            "publisher": "",
            "quantity": 100
        }
        self.update_book_data_no_quantity = {
            "title":"Windmills of Gods",
            "author":"Sidney Sheldon",
            "isbn":"3652472876",
            "publisher": "Publisher",
            "quantity": None
        }
        admin = User('dmwangi@gmail.com', 'dmwangi', 'David', 'Mwangi', 'password1234')
        admin.is_admin = True
        admin.save()
        self.admin_data = {
            "username": "dmwangi",
            "password": "password1234",
        }

    def tearDown(self):
        """Tears down after every test runs"""
        db.session.close()
        db.drop_all()
        self.app_context.pop()

    def register_user(self, data):
        return self.client.post(self.version+'/auth/register', data=json.dumps(data), content_type='application/json')

    def login_user(self, data):
        return self.client.post(self.version+'/auth/login', data=json.dumps(data), content_type='application/json')

    def logout_user(self, user):
        msg = json.loads(user.data)
        print(msg)
        token = msg['Token']
        return self.client.post(self.version+'/auth/logout', headers={"Authorization": "Bearer {}".format(token)})

    def get_all_books(self):
        return self.client.get(self.version+'/books')

    def get_book(self, id):
        return self.client.get(self.version+'/book/' + str(id))

    def login_admin(self):
        return self.login_user(self.admin_data)

    def add_book(self, data):
        admin = self.login_admin()
        token = json.loads(admin.data)['Token']
        return self.client.post(self.version+'/books',
                                data=json.dumps(data), headers={"Authorization": "Bearer {}".format(token)},
                                content_type='application/json')

    def update_book(self, data, id):
        admin = self.login_admin()
        token = json.loads(admin.data)['Token']
        return self.client.put(self.version+'/book/'+str(id), data=json.dumps(data), headers={"Authorization": "Bearer {}".format(token)}, content_type='application/json')

    def delete_book(self, id):
        admin = self.login_admin()
        token = json.loads(admin.data)['Token']
        return self.client.delete(self.version+'/book/'+str(id), headers={"Authorization": "Bearer {}".format(token)}, content_type='application/json')

    def get_all_users(self):
        admin = self.login_admin()
        token = json.loads(admin.data)['Token']
        return self.client.get(self.version+'/users', headers={"Authorization": "Bearer {}".format(token)}, content_type='application/json')

    def review_book(self, id):
        self.register_user(self.user_data)
        user = self.login_user(self.login_data)
        token = json.loads(user.data)['Token']
        return self.client.post(self.version+'/users/books/'+ str(id), headers={"Authorization": "Bearer {}".format(token)}, content_type='application/json')