from django.shortcuts import render
from django.core.serializers import serialize
from django.http import JsonResponse
from .models import WorldBorder

# Page view — just returns the HTML
def world_map(request):
    return render(request, "map/map.html")

# Data view — returns GeoJSON
def world_data(request):
    geojson = serialize("geojson", WorldBorder.objects.all())
    return JsonResponse(geojson, safe=False)