# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.db import migrations
from django.core import management

logger = logging.getLogger(__name__)

def fixture_geonames_countries(apps, schema_editor):
    try:
        management.call_command('synchgeonamescountries', interactive=False)
        management.call_command('synchgeonames', interactive=False)
    except Exception as ex:
        logger.error("fixture_geonames_countries: %s" % str(ex))


class Migration(migrations.Migration):

    dependencies = [
        ('geonames', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fixture_geonames_countries)
    ]
