from django.shortcuts import render
from django.core.serializers import serialize
from django.http import JsonResponse
from .models import WorldBorder
from movies.models import Movie
import json

# Page view — just returns the HTML
def world_map(request):
    return render(request, "map/map.html")

# Data view — returns GeoJSON
def world_data(request):
    # Get all world borders
    borders = WorldBorder.objects.all()
    
    # Serialize to GeoJSON
    geojson_data = json.loads(serialize('geojson', borders, geometry_field='mpoly'))
    
    # Add movie statistics to each country
    for feature in geojson_data['features']:
        country_name = feature['properties']['name']
        
        # Get top movie for this country
        top_movie = get_top_movie_for_country(country_name)
        
        if top_movie:
            feature['properties']['top_movie'] = {
                'name': top_movie['name'],
                'image': top_movie['image'],
                'views': top_movie['views'],
                'orders': top_movie['orders']
            }
        else:
            feature['properties']['top_movie'] = None
    
    return JsonResponse(json.dumps(geojson_data), safe=False)

def get_top_movie_for_country(country_name):
    """Get the most popular movie for a specific country"""
    movies = Movie.objects.all()
    
    top_movie = None
    max_orders = 0
    
    for movie in movies:
        orders = movie.orders_by_region.get(country_name, 0)
        if orders > max_orders:
            max_orders = orders
            top_movie = {
                'name': movie.name,
                'image': movie.image.url if movie.image else '',
                'views': movie.views_by_region.get(country_name, 0),
                'orders': orders
            }
    
    return top_movie