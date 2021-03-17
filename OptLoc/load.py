from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import SwedenCities


# Admin user create
# python manage.py createsuperuser

# Changes in DB Models
# (models.py)
# 1, Prepares db models to be created
#    python manage.py makemigrations
# 2, Creates db models,
#    python manage.py migrate

world_mapping = {
    'namn' : 'NAMN_',
    'knkod' : 'KNKOD',
    'area' : 'AREA',
    'mpoly' : 'MULTIPOLYGON',
}

world_shp = Path(__file__).resolve().parent / 'Swedm' / 'Sweden Municipalties.shp'

def run(verbose=True):
    lm = LayerMapping(SwedenCities, str(world_shp), world_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)