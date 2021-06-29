# -*- coding: utf-8 -*-

import csv
import logging

from zipfile import ZipFile

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Q

from .downloader import Downloader

from geonames.models import Country

logger = logging.getLogger(__name__)


# municipality_levels is a dictionary that tells for some country which adm level holds the municipalities
# http://www.statoids.com/
municipality_levels = {
    'AD': 'GeonamesAdm1',
    'IT': 'GeonamesAdm3',
    'DK': 'GeonamesAdm2',
    'GB': 'PopulatedPlace',
    'FR': 'GeonamesAdm4',
    'NL': 'GeonamesAdm2',
    'BE': 'GeonamesAdm4',
}


class Command(BaseCommand):
    help = '''Synchronize countries data from GeoNames
    '''

    def handle(self, *args, **options):
        base_url = 'https://download.geonames.org/export/dump/'
        # Let's import countries:
        country_dict = {}
        downloader = Downloader()
        if downloader.download(
                source=base_url + "countryInfo.txt",
                destination=settings.GEONAMES_DEST_PATH + "countryInfo.txt",
                force=False
        ):
            # import the country file
            try:
                with open(settings.GEONAMES_DEST_PATH + "countryInfo.txt", 'r') as geonames_file:
                    csv_reader = csv.reader(geonames_file, delimiter='\t', quotechar="\\")
                    for row in csv_reader:
                        if row[0][0] != "#":
                            if Country.objects.filter(code=row[0]).exists():
                                c = Country.objects.get(code=row[0])
                            else:
                                c = Country(code=row[0])
                            c.name=row[4]
                            if c.code in municipality_levels.keys():
                                c.municipality_levels = municipality_levels[c.code]
                            c.save()
                            country_dict[row[0]] = c
            except Exception as ex:
                logger.error("Error %s" % str(ex))
