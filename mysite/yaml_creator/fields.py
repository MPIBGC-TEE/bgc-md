from django.forms import Field,URLField ,DateField
from django.contrib.admin.widgets import AdminDateWidget
from .widgets import FluxesInput
import re

class DOIField(URLField):
    pass
    # we could implement a special validation method here

class PUB_DATEField(DateField):
    widget=AdminDateWidget
    # we could implement a special validation method here

class FluxesField(Field):
    widget = FluxesInput
    #widget = NumberInput
    default_error_messages = {
        'invalid': ('Enter a whole number.'),
    }
    re_decimal = re.compile(r'\.0*\s*$')

    def __init__(self, *, max_value=None, min_value=None, **kwargs):
        super().__init__(**kwargs)

        #if max_value is not None:
        #    self.validators.append(validators.MaxValueValidator(max_value))
        #if min_value is not None:
        #    self.validators.append(validators.MinValueValidator(min_value))

    def to_python(self, value):
        """
        """
        print("########## value")
        print(value)
        #value = super().to_python(value)
        #fake values
        #value= [
		#	[{"source":0},{"target":0},{}],
		#	[{"source":1},{"target":0},{}],
		#	[{"source":2},{"target":0},{}],
		#	[{"source":3},{"target":0},{}]
        #]
        return value

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        if isinstance(widget, FluxesInput):
            attrs['test'] = 42
        return attrs
