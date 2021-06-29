# -*- coding: utf-8 -*-

import csv
import logging

from zipfile import ZipFile

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Q

from .downloader import Downloader

from geonames.models import Country, GeonamesAdm1, GeonamesAdm2, GeonamesAdm3, GeonamesAdm4, GeonamesAdm5, PopulatedPlace

logger = logging.getLogger(__name__)

# municipality_levels is a dictionary that tells for some country which adm level holds the municipalities
# http://www.statoids.com/
municipality_levels = settings.MUNICIPALITY_LEVELS

# m is a dictionary mapping Italian municipalities names for ISTAT into names for geonames
m = {}
m["Campiglione Fenile"] = "Campiglione-Fenile"
m["Leini"] = "Leinì"
m["Mappano"] = ""
m["Castellinaldo d'Alba"] = "Castellinaldo"
m["Cerretto Langhe"] = "Cerreto Langhe"
m["Fubine Monferrato"] = "Fubine"
m["Châtillon"] = "Chatillon"
m["Hône"] = "Hone"
m["Jovençan"] = "Jovencan"
m["Rhêmes-Notre-Dame"] = "Rhemes-Notre-Dame"
m["Rhêmes-Saint-Georges"] = "Rhemes-Saint-Georges"
m["Gornate Olona"] = "Gornate-Olona"
m["Costa Serina"] = "Costa di Serina"
m["Lonato del Garda"] = "Lonato"
m["Rodengo Saiano"] = "Rodengo-Saiano"
m["Tremosine sul Garda"] = "Tremosine"
m["Godiasco Salice Terme"] = "Godiasco"
m["Rivanazzano Terme"] = "Rivanazzano"
m["Corvara in Badia"] = "Corvara in Badia - Corvara"
m["Gais"] = "Gais - Gais"
m["Lana"] = "Lana - Lana"
m["Lasa"] = "Lasa - Laas"
m["Ora"] = "Ora - Auer"
m["Ortisei"] = "Ortisei - St. Ulrich"
m["Parcines"] = "Partschins - Parcines"
m["Postal"] = "Postal - Burgstall"
m["Prato allo Stelvio"] = "Prato allo Stelvio - Prad am Stilfser Joch"
m["Racines"] = "Racines - Ratschings"
m["Rio di Pusteria"] = "Rio di Pusteria - Muehlbach"
m["Rodengo"] = "Rodengo - Rodeneck"
m["San Candido"] = "San Candido - Innichen"
m["San Genesio Atesino"] = "San Genesio Atesino - Jenesien"
m["San Leonardo in Passiria"] = "San Leonardo in Passiria - St. Leonhard in Passeier"
m["San Lorenzo di Sebato"] = "San Lorenzo di Sebato - St. Lorenzen"
m["San Martino in Badia"] = "San Martino in Badia - St. Martin in Thurn"
m["Selva dei Molini"] = "Selva dei Molini - Muehlwald"
m["Terento"] = "Terento - Terenten"
m["Trodena nel parco naturale"] = "Trodena"
m["Tubre"] = "Tubre - Taufers im Muenstertal"
m["Varna"] = "Varna - Vahrn"
m["Costermano sul Garda"] = "Costermano"
m["Soraga di Fassa"] = "Soraga"
m["Brenzone sul Garda"] = "Brenzone"
m["San Stino di Livenza"] = "Santo Stino di Livenza"
m["Vo'"] = "Vò"
m["Duino-Aurisina"] = "Duino Aurisina"
m["San Dorligo della Valle-Dolina"] = "San Dorligo della Valle"
m["Aquila d'Arroscia"] = "Aquila di Arroscia"
m["Cosio d'Arroscia"] = "Cosio di Arroscia"
m["Genova"] = "Genoa"
m["Luni"] = "Ortonovo"
m["Montescudo-Monte Colombo"] = "Montescudo - Montecolombo"
m["Civitella Paganico"] = "Civitella-Paganico"
m["Roma"] = "Roma Capitale"
m["San Giorgio La Molara"] = "San Giorgio la Molara"
m["Cassano all'Ionio"] = "Cassano allo Ionio"
m["San Vincenzo La Costa"] = "San Vincenzo la Costa"
m["Casali del Manco"] = ""
m["Reggio di Calabria"] = "Reggio Calabria"
m["Ionadi"] = "Jonadi"
m["Donori"] = "Donorì"


class ICity:
    """
    City field indexes in geonames.
    Description of fields: https://download.geonames.org/export/dump/readme.txt
    """
    geonameid = 0
    name = 1
    asciiName = 2
    alternateNames = 3
    latitude = 4
    longitude = 5
    featureClass = 6
    featureCode = 7
    countryCode = 8
    cc2 = 9
    admin1Code = 10
    admin2Code = 11
    admin3Code = 12
    admin4Code = 13
    population = 14
    elevation = 15
    gtopo30 = 16
    timezone = 17
    modificationDate = 18


class IComuneItaliano:
    """
    ComuneItaliano field indexes in ISTAT.
    """
    Codice_Regione = 0
    Codice_Città_Metropolitana = 1
    Codice_Provincia_1 = 2
    Progressivo_del_Comune_2 = 3
    Codice_Comune_formato_alfanumerico = 4
    Denominazione_in_italiano = 5
    Denominazione_in_tedesco = 6
    Codice_Ripartizione_Geografica = 7
    Ripartizione_geografica = 8
    Denominazione_regione = 9
    Denominazione_Città_metropolitana = 10
    Denominazione_provincia = 11
    Flag_Comune_capoluogo_di_provincia = 12
    Sigla_automobilistica = 13
    Codice_Comune_formato_numerico = 14
    Codice_Comune_numerico_con_110_province_dal_2010_al_2016 = 15
    Codice_Comune_numerico_con_107_province_dal_2006_al_2009 = 16
    Codice_Comune_numerico_con_103_province_dal_1995_al_2005 = 17
    Codice_Catastale_del_comune = 18
    Popolazione_legale_2011_09_10_2011 = 19
    Codice_NUTS1_2010 = 20
    Codice_NUTS2_2010_3_ = 21
    Codice_NUTS3_2010 = 22
    Codice_NUTS1_2006 = 23
    Codice_NUTS2_2006_3 = 24
    Codice_NUTS3_2006 = 25


class Command(BaseCommand):
    help = '''Synchronize data from GeoNames
    '''

    def handle(self, *args, **options):
        log_every_n_records = 1000
        n_records = 0
        base_url = 'https://download.geonames.org/export/dump/'
        countries = settings.GEONAMES_INCLUDE_COUNTRIES
        countries_excluded = settings.GEONAMES_EXCLUDE_INSERT_COUNTRIES
        # Let's create country dictionary to save some queries:
        country_dict = {}
        for c in Country.objects.filter(code__in=countries):
            country_dict[c.code] = c
        try:
            # download the files
            for c in countries:
                if c not in countries_excluded:
                    downloader = Downloader()
                    if downloader.download(
                            source=base_url + c + ".zip",
                            destination=settings.GEONAMES_DEST_PATH + c + ".zip",
                            force=False
                    ):
                        # extract the file
                        zip_path = settings.GEONAMES_DEST_PATH + c + ".zip"
                        with ZipFile(zip_path, 'r') as myzip:
                            myzip.extract(c + ".txt", settings.GEONAMES_DEST_PATH)
            # Let's import them
            logger.debug("synchgeonames countries_excluded %s" % countries_excluded)
            for c in countries:
                current_country_m_level = 0
                if municipality_levels[c] == 'PopulatedPlace':
                    current_country_m_level = 5
                elif municipality_levels[c][:len('GeonamesAdm')] == 'GeonamesAdm':
                    current_country_m_level = int(municipality_levels[c][len('GeonamesAdm'):])
                if current_country_m_level == 0:
                    logger.warning("Country %s has no setting for municipality level" % c.code)
                current_country = Country.objects.get(code=c)
                if (c not in countries_excluded) and not current_country.data_loaded:
                    logger.debug("synchgeonames importing %s %s" % (c, settings.GEONAMES_DEST_PATH + c + ".txt"))
                    with open(settings.GEONAMES_DEST_PATH + c + ".txt", 'r') as geonames_file:
                        csv_reader = csv.reader(geonames_file, delimiter='\t', quotechar="\\")
                        # Let's work on adm1 first
                        adm1_dict = {}
                        for row in csv_reader:
                            if row[ICity.featureCode] in settings.GEONAMES_ADM_TYPES and \
                                    row[ICity.featureCode] == 'ADM1' \
                                    and current_country_m_level>=1:
                                if n_records % log_every_n_records == 0:
                                    logger.debug(
                                        "synchgeonames importing adm1 %s %s. %s records" % (row[ICity.countryCode], row[ICity.name], n_records))
                                n_records += 1
                                try:
                                    adm = GeonamesAdm1(name=row[ICity.name], code=row[ICity.admin1Code],
                                                       country=country_dict[row[ICity.countryCode]])
                                    adm.save()
                                    adm1_dict[row[ICity.admin1Code]] = adm
                                except Exception as ex:
                                    logger.error("Saving adm1 - %s - %s" % (str(ex), str(row)))
                        # adm2
                        adm2_dict = {}
                        geonames_file.seek(0)
                        for row in csv_reader:
                            if row[ICity.featureCode] in settings.GEONAMES_ADM_TYPES and \
                                    row[ICity.featureCode] == 'ADM2'\
                                    and current_country_m_level>=2:
                                if n_records % log_every_n_records == 0:
                                    logger.debug(
                                        "synchgeonames importing adm2 %s %s. %s records" % (
                                            row[ICity.countryCode], row[ICity.name], n_records))
                                n_records += 1
                                try:
                                    adm = GeonamesAdm2(name=row[ICity.name], code=row[ICity.admin2Code],
                                                       adm1=adm1_dict[row[ICity.admin1Code]])
                                    adm.save()
                                    adm2_dict[row[ICity.admin2Code]] = adm
                                except Exception as ex:
                                    logger.error("Saving adm2 - %s - %s" % (str(ex), str(row)))
                        # adm3
                        adm3_dict = {}
                        geonames_file.seek(0)
                        for row in csv_reader:
                            if row[ICity.featureCode] in settings.GEONAMES_ADM_TYPES and \
                                    row[ICity.featureCode] == 'ADM3'\
                                    and current_country_m_level>=3:
                                if n_records % log_every_n_records == 0:
                                    logger.debug(
                                        "synchgeonames importing adm3 %s %s. %s records" % (
                                            row[ICity.countryCode], row[ICity.name], n_records))
                                n_records += 1
                                try:
                                    adm = GeonamesAdm3(name=row[ICity.name], code=row[ICity.admin3Code],
                                                       adm2=adm2_dict[row[ICity.admin2Code]])
                                    adm.save()
                                    adm3_dict[row[ICity.admin3Code]] = adm
                                except Exception as ex:
                                    logger.error("Saving adm3 - %s - %s" % (str(ex), str(row)))

                        # adm4
                        adm4_dict = {}
                        geonames_file.seek(0)
                        for row in csv_reader:
                            if row[ICity.featureCode] in settings.GEONAMES_ADM_TYPES and \
                                    row[ICity.featureCode] == 'ADM4'\
                                    and current_country_m_level>=4:
                                if n_records % log_every_n_records == 0:
                                    logger.debug(
                                        "synchgeonames importing adm4 %s %s. %s records" % (
                                            row[ICity.countryCode], row[ICity.name], n_records))
                                n_records += 1
                                try:
                                    if row[ICity.admin3Code]:
                                        adm = GeonamesAdm4(name=row[ICity.name], code=row[ICity.admin4Code],
                                                           adm3=adm3_dict[row[ICity.admin3Code]])
                                        adm.save()
                                        adm4_dict[row[ICity.admin4Code]] = adm
                                    elif row[ICity.admin2Code]:
                                        adm = GeonamesAdm4(name=row[ICity.name], code=row[ICity.admin4Code],
                                                           adm2=adm2_dict[row[ICity.admin2Code]])
                                        adm.save()
                                        adm4_dict[row[ICity.admin4Code]] = adm
                                    else:
                                        logger.warning("%s %s %s has neither admin3Code nor admin2Code" %
                                                       (row[ICity.name], row[ICity.featureCode], row[ICity.admin4Code]))
                                except Exception as ex:
                                    logger.error("Saving adm4 - %s - %s" % (str(ex), str(row)))
                        # adm5
                        geonames_file.seek(0)
                        for row in csv_reader:
                            if row[ICity.featureCode] in settings.GEONAMES_ADM_TYPES and \
                                    row[ICity.featureCode] == 'ADM5'\
                                    and current_country_m_level>=5:
                                if n_records % log_every_n_records == 0:
                                    logger.debug(
                                        "synchgeonames importing adm5 %s %s. %s records" % (row[ICity.countryCode], row[ICity.name], n_records))
                                n_records += 1
                                try:
                                    adm = GeonamesAdm5(name=row[ICity.name], adm4=adm4_dict[row[ICity.admin4Code]])
                                    adm.save()
                                except Exception as ex:
                                    logger.error("Saving adm5 - %s - %s" % (str(ex), str(row)))
                        # populated places
                        geonames_file.seek(0)
                        for row in csv_reader:
                            if row[ICity.featureCode] in settings.GEONAMES_INCLUDE_CITY_TYPES \
                                    and current_country_m_level>=5:
                                if n_records % log_every_n_records == 0:
                                    logger.debug(
                                        "synchgeonames importing ppl %s %s. %s records" % (row[ICity.countryCode], row[ICity.name], n_records))
                                n_records += 1
                                try:
                                    pp = PopulatedPlace(name=row[ICity.name], feature_code=row[ICity.featureCode],
                                                        country=country_dict[row[ICity.countryCode]])
                                    if row[ICity.admin1Code]:
                                        try:
                                            pp.adm1 = adm1_dict[row[ICity.admin1Code]]
                                        except:
                                            pass
                                    if row[ICity.admin2Code]:
                                        try:
                                            pp.adm2 = adm2_dict[row[ICity.admin2Code]]
                                        except:
                                            pass
                                    if row[ICity.admin3Code]:
                                        try:
                                            pp.adm3 = adm3_dict[row[ICity.admin3Code]]
                                        except:
                                            pass
                                    if row[ICity.admin4Code]:
                                        try:
                                            pp.adm4 = adm4_dict[row[ICity.admin4Code]]
                                        except:
                                            pass
                                    pp.save()
                                except Exception as ex:
                                    logger.error("Saving PopulatedPlace - %s - %s" % (str(ex), str(row)))

                        current_country.data_loaded = True
                        current_country.save()
                if c == 'IT' and c not in countries_excluded:
                    '''
                    '   I use the permalink to the ISTAT list of Italian municipalities to add to adm3 the field 
                    '   Codice Catastale
                    '''
                    istat_permalink = "https://www.istat.it/storage/codici-unita-amministrative/Elenco-comuni-italiani.csv"
                    downloader = Downloader()
                    if downloader.download(
                            source=istat_permalink,
                            destination=settings.GEONAMES_DEST_PATH + "Elenco-comuni-italiani.csv",
                            force=False
                    ):
                        with open(settings.GEONAMES_DEST_PATH + "Elenco-comuni-italiani.csv", 'r', encoding = "ISO-8859-1") as istat_file:
                            csv_reader = csv.reader(istat_file, delimiter=';', quotechar="\\")
                            digits_as_string = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                            for row in csv_reader:
                                # Let's loop on data from ISTAT
                                # if first column value is a number
                                if len(row[0]) and row[0][0] in digits_as_string:
                                    # and search on existing geonames records
                                    '''
                                    '   Year 2017, Sardinian towns have changed province, we try filtering just on names
                                    '   if we find more than one record we also filter on province (this case won't work
                                    '   with Sardinian towns, that's why we try it as a second option)
                                    '''
                                    # Some italian names are different so there is a mapping dictionary
                                    italian_name = row[IComuneItaliano.Denominazione_in_italiano]
                                    if italian_name in m.keys() and m[italian_name] != "":
                                        italian_name = m[italian_name]
                                    if GeonamesAdm3.objects.filter(
                                                    Q(name=italian_name)|
                                                    Q(name=row[IComuneItaliano.Denominazione_in_tedesco])
                                    ).exists():
                                        try:
                                            if GeonamesAdm3.objects.filter(
                                                            Q(name=italian_name)|
                                                            Q(name=row[IComuneItaliano.Denominazione_in_tedesco])
                                            ).count() == 1:
                                                adm3 = GeonamesAdm3.objects.get(
                                                    Q(name=italian_name) |
                                                    Q(name=row[IComuneItaliano.Denominazione_in_tedesco])
                                                )
                                            else:
                                                adm3 = GeonamesAdm3.objects.filter(
                                                    Q(name=italian_name)|
                                                    Q(name=row[IComuneItaliano.Denominazione_in_tedesco])
                                                ).get(adm2__code=row[IComuneItaliano.Sigla_automobilistica])
                                            adm3.name = row[IComuneItaliano.Denominazione_in_italiano]
                                            # Let's use ISTAT names ( geonames has Genoa instead of Genova, ISTAT has
                                            # it right )
                                            adm3.it_codice_catastale = row[IComuneItaliano.Codice_Catastale_del_comune]
                                            adm3.save()
                                        except Exception as ex:
                                            logger.error(
                                                "%s-%s is in ISTAT's Elenco-comuni-italiani.csv. In Adm3 gave error: %s"
                                                % (italian_name,
                                                   row[IComuneItaliano.Denominazione_in_tedesco], str(ex)))
                                    else:
                                        logger.warning("%s-%s is in ISTAT's Elenco-comuni-italiani.csv but not in Adm3"
                                                       % (row[IComuneItaliano.Denominazione_in_italiano],
                                                          italian_name))


        except Exception as ex:
            logger.error("Error %s - %s" % (str(ex), str(row)))
        pass