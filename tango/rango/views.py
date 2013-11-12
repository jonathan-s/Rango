from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from rango.models import Category, Page

def category(request, category_name_url):
    context = RequestContext(request)

    category_name = category_name_url.replace('_', ' ')

    context_dict = {'category_name': category_name}

    try:
        category = Category.objects.get(name=category_name)

        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass
    return render_to_response('rango/category.html', context_dict, context)


def index(request):
    # Request the cotext of the request.
    # The context contains information such as the client's machine details, for example
    context = RequestContext(request)

    # construct a dictionary to pass to the template engine as its context. 
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}
    
    for category in category_list:
        category.url = category.name.replace(' ', '_')

    return render_to_response('rango/index.html', context_dict, context)

def about(request):
    return HttpResponse("Rango says: Here is the about page.")