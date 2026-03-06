from marshmallow import Schema, fields, validate, validates, ValidationError
from src.models.admin import Admin
import datetime


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6,max=8))

    @validates('email')
    def validate_email(self, value, **kwargs):
        if not value.endswith('@gmail.com') and not value.endswith('@yahoo.com'):
            raise ValidationError('Email must be a valid gmail or yahoo address.')

class RegisterSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
        