#-*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.forms.fields import CharField
from django.core.exceptions import ValidationError
from phonenumber_field.validators import validate_international_phonenumber
from phonenumbers.phonenumberutil import NumberParseException
from phonenumber_field.phonenumber import PhoneNumber, to_python


class PhoneNumberField(CharField):
    default_error_messages = {
        'invalid': _(u'Enter a valid phone number (e.g. +41421234567).'),
    }
    default_validators = [validate_international_phonenumber]

    def to_python(self, value):
        phone_number = to_python(value)
        if phone_number and not phone_number.is_valid():
            raise ValidationError(self.error_messages['invalid'])
        return phone_number