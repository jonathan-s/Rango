from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

from datetime import datetime

from rango.bing_search import run_query



def decode_url(url):
    name = url.replace('_', ' ')
    return name



# //////////////// Form Views /////////////////

def register(request):
    context = RequestContext(request)

    registered = False

    # Post request
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save() # does this really save form data to the database?

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save() 
            registered = True
        else:
            print user_form.errors, profile_form.errors
    # not a HTTP POST
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # render template 
    return render_to_response('rango/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}, context)

def add_page(request, category_name_url):
    context = RequestContext(request)

    category_name = decode_url(category_name_url)

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():

            page = form.save(commit=False)

            cat = Category.objects.get(name=category_name)
            page.category = cat

            page.views = 0

            page.save()
            return category(request, category_name_url)
        else:
            print form.errors
    else:
        form = PageForm()

    return render_to_response('rango/add_page.html', {'category_name_url': category_name_url, 'category_name': category_name, 'form': form }, context)



def add_category(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        # if request was a GET, display form to enter details. 
        form = CategoryForm()
    return render_to_response('rango/add_category.html', {'form': form }, context)




# //////////////// Regular Views //////////////

def about(request):
    context = RequestContext(request)

    visits = request.session.get('visits', 0)

    return render_to_response('rango/about.html', {'visits': visits}, context)

def category(request, category_name_url):
    context = RequestContext(request)

    category_name = decode_url(category_name_url)

    context_dict = {'category_name': category_name, 'category_name_url': category_name_url}

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

    if request.session.get('last_visit'):
        last_visit = request.session.get('last_visit')
        visits = request.session.get('visits', 0)
        print last_visit
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).days > 0:
            request.session['visits'] = visits + 1
            request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1

    return render_to_response('rango/index.html', context_dict, context)

def search(request):
    context = RequestContext(request)
    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            result_list = run_query(query)

    return render_to_response('rango/search.html', {'result_list': result_list}, context)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')

def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user: # don't need if user is not None 
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your Rango account is disabled")
        else:
            print "Invalid login details {0}, {1}".format(username, password)
            return HttpResponse("Invalid Login details supplied")
    else: 
        return render_to_response("rango/login.html", {}, context)







