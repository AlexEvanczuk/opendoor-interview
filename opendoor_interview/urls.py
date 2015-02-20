from django.conf.urls import patterns, include, url
from predict_house_prices import views
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'opendoor_interview.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='app.html')),
    url(r'^loaddata/', views.load_data),
    url(r'^returnhouses/', views.return_houses),
    url(r'^returnhousebubbles/', views.return_house_bubbles),
    url(r'^returnclusters/', views.return_clusters),
    url(r'^linearmodel/', views.linear_model),
    url(r'^loadcities/', views.load_cities),
    url(r'^loadclusters/', views.cluster_data)

)
