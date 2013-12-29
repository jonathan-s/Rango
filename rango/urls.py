from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
    url(r'^about/', views.about, name="about"),
    url(r'^$', views.index, name="index"),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_url>\w+)/$', views.category, name='category'),
    url(r'^category/(?P<category_name_url>\w+)/add_page$', views.add_page, name="add_page"), 
    url(r'^category_like/', views.category_like, name="category_like"),
    url(r'^category_suggest/', views.category_suggest, name="category_suggest"),
    url(r'^register/$', views.register, name="register"),
    url(r'^login/$', views.user_login, name="login"),
    url(r'^logout/$', views.user_logout, name="logout"),
    #url(r'^search/$', views.search, name="search"),
    url(r'^goto/', views.track_url, name="track_url"),
    url(r'^profile/$', views.profile, name="profile"),
)