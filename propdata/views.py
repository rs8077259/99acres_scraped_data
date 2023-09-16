from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import utils
from .form import PropertyFilterForm

def filter_properties(request):
    if request.method == 'POST':
        form = PropertyFilterForm(request.POST)
        if form.is_valid():
            property_data = form.cleaned_data['property_data']
    db=utils.client.soup
    form = PropertyFilterForm()
    context={
        'data':db.scrap.find({"propertyCity":property_data}),
        'form': form
    }
    tamplate=loader.get_template("showdata.html")
    return HttpResponse(tamplate.render(context,request))

def index(request):
    db=utils.client.soup
    form = PropertyFilterForm()
    context={
        'data':db.scrap.find(),
        'form': form
    }
    tamplate=loader.get_template("showdata.html")
    return HttpResponse(tamplate.render(context,request))
