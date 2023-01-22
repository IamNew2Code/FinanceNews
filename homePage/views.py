from django.shortcuts import render
from homePage.models import Video
'''
from alpha_vantage.timeseries import TimeSeries
import requests
#Attempt to put a stock or crypto graph on the homepage
    API_key = 'CJC7PFQ4VETDAT8Z'

    ts = TimeSeries(key=API_key, output_format='pandas')

    data, meta = ts.get_intraday('TSLA', interval='1min',outputsize='full')
'''
def home_screen_view(request):

    
    context = {}
    videos = Video.objects.all()
    context['videos'] = videos

    return render(request, 'homePage/home.html',context)
