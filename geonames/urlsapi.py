#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url

from geonames import api

urlpatterns = [

    #36:
    url( r'^countries/$', api.countries, name='countries'),
    url( r'^municipalities/$', api.municipalities, name='municipalities'),
]