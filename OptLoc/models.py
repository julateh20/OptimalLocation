from django.db import models

# Create your models here.
from django.contrib.gis.db import models

class SwedenCities(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    namn  = models.CharField(max_length=50)
    knkod = models.CharField(max_length=4)
    area = models.FloatField()

    # KNKOD: String(4.0)
    # AREA: Real(19.11)
    # NAMN_: String(30.0)
    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.namn