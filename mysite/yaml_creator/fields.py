from django.forms import URLField
from django.forms import DateField
from django.contrib.admin.widgets import AdminDateWidget

class DOIField(URLField):
    pass
    # we could implement a special validation method here

class PUB_DATEField(DateField):
    widget=AdminDateWidget
    # we could implement a special validation method here