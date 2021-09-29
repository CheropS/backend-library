from cerberus import Validator

def validate_register(data):
    schema = {
        'email': {
            'type': 'string',
            'regex': '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
            'required': True,
            'empty': False,
            'maxlength': 60
        },
        'username': {
            'type': 'string',
            'required': True,
            'empty': False,
            'maxlength': 60
        },
        'first_name': {
            'type': 'string',
            'required': True,
            'empty': False,
            'maxlength': 60
        },
        'last_name': {
            'type': 'string',
            'required': True,
            'empty': False,
            'maxlength': 60
        },
        'password': {
            'type': 'string',
            # 'regex': '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$',
            'required': True,
            'minlength': 8,
            'empty': False,
            'maxlength': 20
        },
        'confirm_password': {
            'type': 'string',
            # 'regex': '',
            'required': True,
            'empty': False,
            'maxlength': 20
        }
    }
    validator = Validator(schema)
    validator.validate(data)
    errors = validator.errors
    if errors:
        return errors
    data['email'] = data['email'].replace(" ", "").lower()
    data['username'] = data['username'].replace(" ", "").lower()
    data['first_name'] = data['first_name'].replace(" ", "")
    data['last_name'] = data['last_name'].replace(" ", "")

def validate_login(data):
    schema = {
        'username': {
            'type': 'string',
            'required': True,
            'empty': False
        },
        'password': {
            'type': 'string',
            'required': True,
            'empty': False
        }
    }
    validator = Validator(schema)
    validator.validate(data)
    errors = validator.errors
    if errors:
        return errors

def validate_reset(data):
    schema = {
        'password': {
            'type': 'string',
            'required': True
        },
        'new_password': {
            'type': 'string',
            'required': True
        },
        'confirm_password': {
            'type': 'string',
            'required': True
        }
    }
    validator = Validator(schema)
    validator.validate(data)
    errors = validator.errors
    if errors:
        return errors
