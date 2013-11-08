from django.http import HttpResponse

def index(request):
    return HttpResponse("""
        Rango says hello world<br>
        And a link to <a href="about/">about</a>
        """)

def about(request):
    return HttpResponse("Rango says: Here is the about page.")