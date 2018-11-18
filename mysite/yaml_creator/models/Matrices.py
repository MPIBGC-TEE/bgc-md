from django.db import models
from . FluxRepresentation import FluxRepresentation

class Matrices(FluxRepresentation):
    A=models.CharField(max_length=2000)

