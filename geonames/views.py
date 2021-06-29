# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
	Country,
	GeonamesAdm1,
	GeonamesAdm2,
	GeonamesAdm3,
	GeonamesAdm4,
	GeonamesAdm5,
	PopulatedPlace,
)


class CountryCreateView(CreateView):

    model = Country


class CountryDeleteView(DeleteView):

    model = Country


class CountryDetailView(DetailView):

    model = Country


class CountryUpdateView(UpdateView):

    model = Country


class CountryListView(ListView):

    model = Country


class GeonamesAdm1CreateView(CreateView):

    model = GeonamesAdm1


class GeonamesAdm1DeleteView(DeleteView):

    model = GeonamesAdm1


class GeonamesAdm1DetailView(DetailView):

    model = GeonamesAdm1


class GeonamesAdm1UpdateView(UpdateView):

    model = GeonamesAdm1


class GeonamesAdm1ListView(ListView):

    model = GeonamesAdm1


class GeonamesAdm2CreateView(CreateView):

    model = GeonamesAdm2


class GeonamesAdm2DeleteView(DeleteView):

    model = GeonamesAdm2


class GeonamesAdm2DetailView(DetailView):

    model = GeonamesAdm2


class GeonamesAdm2UpdateView(UpdateView):

    model = GeonamesAdm2


class GeonamesAdm2ListView(ListView):

    model = GeonamesAdm2


class GeonamesAdm3CreateView(CreateView):

    model = GeonamesAdm3


class GeonamesAdm3DeleteView(DeleteView):

    model = GeonamesAdm3


class GeonamesAdm3DetailView(DetailView):

    model = GeonamesAdm3


class GeonamesAdm3UpdateView(UpdateView):

    model = GeonamesAdm3


class GeonamesAdm3ListView(ListView):

    model = GeonamesAdm3


class GeonamesAdm4CreateView(CreateView):

    model = GeonamesAdm4


class GeonamesAdm4DeleteView(DeleteView):

    model = GeonamesAdm4


class GeonamesAdm4DetailView(DetailView):

    model = GeonamesAdm4


class GeonamesAdm4UpdateView(UpdateView):

    model = GeonamesAdm4


class GeonamesAdm4ListView(ListView):

    model = GeonamesAdm4


class GeonamesAdm5CreateView(CreateView):

    model = GeonamesAdm5


class GeonamesAdm5DeleteView(DeleteView):

    model = GeonamesAdm5


class GeonamesAdm5DetailView(DetailView):

    model = GeonamesAdm5


class GeonamesAdm5UpdateView(UpdateView):

    model = GeonamesAdm5


class GeonamesAdm5ListView(ListView):

    model = GeonamesAdm5


class PopulatedPlaceCreateView(CreateView):

    model = PopulatedPlace


class PopulatedPlaceDeleteView(DeleteView):

    model = PopulatedPlace


class PopulatedPlaceDetailView(DetailView):

    model = PopulatedPlace


class PopulatedPlaceUpdateView(UpdateView):

    model = PopulatedPlace


class PopulatedPlaceListView(ListView):

    model = PopulatedPlace

