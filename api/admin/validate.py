from cerberus import Validator
from flask import Response, json


def validate_book(data):
    schema = {
        'title': {
            'type': 'string',
            'required': True,
            'empty': False,
            'maxlength': 500
        },
        'author': {
            'type': 'string',
            'required': True,
            'empty': False,
            'maxlength': 100
        },
        'isbn': {
            'type': 'string',
            'required': True,
            'empty': False,
            'maxlength': 100
        },
        'publisher': {
            'type': 'string',
            'empty': False,
            'maxlength': 100
        },
        'quantity': {
            # 'type': 'integer',
            'empty': False,
            'required': True
        }
    }
    validator = Validator(schema)
    validator.validate(data)
    errors = validator.errors
    if errors:
        return errors
    data['title'] = data['title'].strip().lower().title()
    data['author'] = data['author'].strip().title()
    data['isbn'] = data['isbn'].strip()
    data['publisher'] = data['publisher'].strip().title()


def validate_arg(arg):
    try:
        arg = int(arg)
    except Exception as e:
        return Response(json.dumps({"Message": "Invalid argument passed"}), status=400)
