from django import forms

import bleach


class SanitizedCharField(forms.CharField):
    """
    A subclass of CharField that escapes (or strip) HTML tags and attributes.
    """    
    def __init__(self, allowed_tags=[], allowed_attributes=[], strip=False, *args, **kwargs):
        self._allowed_tags = allowed_tags
        self._allowed_attributes = allowed_attributes
        self._strip = strip
        super(SanitizedCharField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(SanitizedCharField, self).clean(value)
        return bleach.clean(value, tags=self._allowed_tags,
            attributes=self._allowed_attributes, strip=self._strip)
