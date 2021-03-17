from django.shortcuts import render
from OptLoc.optimalLocation import OptimalLocationModel
# Create your views here.
from django.http import HttpResponse

def index(request):

    # Backend process
    [City, optLoc] = OptimalLocationModel.CalculateOptimalLocation(1001)
    # You can access database - GEODjango

    # Display result - optimal location
    return render(request, 'OptLoc.html',
                  {'Optimal_Location': optLoc,
                   'Optimal_City': City} )