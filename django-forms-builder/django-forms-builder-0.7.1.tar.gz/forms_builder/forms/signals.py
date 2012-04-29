
from django.dispatch import Signal

form_invalid = Signal(providing_args=["form"])
form_valid = Signal(providing_args=["form", "entry"])
