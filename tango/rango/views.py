from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    # Request the cotext of the request.
    # The context contains information such as the client's machine details, for example
    context = RequestContext(request)

    # construct a dictionary to pass to the template engine as its context. 
    context_dict = {'boldmessage': 'I am from the context'}
    return render_to_response('rango/index.html', context_dict, context)

def about(request):
    return HttpResponse("Rango says: Here is the about page.")