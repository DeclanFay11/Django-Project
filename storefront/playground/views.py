from django.shortcuts import render
from django.http import HttpResponse
from .vessel_scripts import marinetraffic_vessels_in_port

# Create your views here.
# View function takes a request and returns a response 
# request handler
# action

def home(request):
    #return HttpResponse("Hello World")
    return render(request, 'home.html')

def say_hello(request):
    #return HttpResponse("Hello World")
    return render(request, 'hello.html',{'name': 'Declan'})

def testView(request):
    return render(request,'test.html')

def print_to_terminal(request):
    marinetraffic_vessels_in_port()
    #print("Declan Fay")
    return render(request,'home.html')