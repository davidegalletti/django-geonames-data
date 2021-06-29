from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    code = models.CharField(max_length=20, db_index=True)
    # municipality_levels is a list of strings blank-separated with
    # possible values GeonamesAdm1-GeonamesAdm5, PopulatedPlace
    # and tells which models hold the municipalities for this country
    # For Italy the town of Pisa is (and all the others are)
    # Adm3 so municipality_levels for Italy has to be GeonamesAdm3
    # GB has likely cities in two levels 2 and 3: we use a string like "GeonamesAdm2 GeonamesAdm3"
    # or in 3 and PPL hence "GeonamesAdm3 PopulatedPlace"
    municipality_levels = models.CharField(max_length=200, default='')
    # data_loaded is True if we have loaded from geonames data for this country
    data_loaded = models.BooleanField(default=False, db_index=True)
    # Foreign countries have a code used to calculate Italian Codice Fiscale
    it_codice_catastale = models.CharField(max_length=4, blank=True, null=True)

    def __str__(self):
        return self.name


class GeonamesAdm(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    alternate_names = models.CharField(max_length=2000, default='', db_index=True)
    suppressed = models.BooleanField(default=True)

    class Meta:
        abstract = True


class GeonamesAdm1(GeonamesAdm):
    code = models.CharField(max_length=20, db_index=True)
    feature_code = models.CharField(max_length=20)
    country = models.ForeignKey(Country)

    def __str__(self):
        return self.name


class GeonamesAdm2(GeonamesAdm):
    code = models.CharField(max_length=20, db_index=True)
    feature_code = models.CharField(max_length=20)
    adm1 = models.ForeignKey(GeonamesAdm1)

    @property
    def country(self):
        return self.adm1.country

    def __str__(self):
        return self.name


class GeonamesAdm3(GeonamesAdm):
    code = models.CharField(max_length=20, db_index=True)
    adm2 = models.ForeignKey(GeonamesAdm2)
    postal_code = models.CharField("Postal Code", max_length=10)
    # Italian municipalities are adm3 and have a code used to calculate Codice Fiscale
    it_codice_catastale = models.CharField(max_length=4, blank=True, null=True)

    @property
    def country(self):
        return self.adm2.country

    def __str__(self):
        return self.name


class GeonamesAdm4(GeonamesAdm):
    code = models.CharField(max_length=20, db_index=True)
    # GB has some ADM4 with adm2 parent and without adm3
    adm2 = models.ForeignKey(GeonamesAdm2, blank=True, null=True)
    adm3 = models.ForeignKey(GeonamesAdm3, blank=True, null=True)

    @property
    def country(self):
        if self.adm2:
            return self.adm2.country
        else:
            return self.adm3.country

    def __str__(self):
        return self.name


class GeonamesAdm5(GeonamesAdm):
    adm4 = models.ForeignKey(GeonamesAdm4)

    @property
    def country(self):
        return self.adm4.country

    def __str__(self):
        return self.name


class PopulatedPlace(GeonamesAdm):
    feature_code = models.CharField(max_length=20, db_index=True)
    country = models.ForeignKey(Country)
    adm1 = models.ForeignKey(GeonamesAdm1, blank=True, null=True)
    adm2 = models.ForeignKey(GeonamesAdm2, blank=True, null=True)
    adm3 = models.ForeignKey(GeonamesAdm3, blank=True, null=True)
    adm4 = models.ForeignKey(GeonamesAdm4, blank=True, null=True)

    def __str__(self):
        return self.name
