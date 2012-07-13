from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView

sqs = SearchQuerySet().facet('type').facet('location')

urlpatterns = patterns('haystack.views',
    url(r'^$', FacetedSearchView(form_class=FacetedSearchForm, searchqueryset=sqs), name='haystack_search'),
)

urlpatterns = urlpatterns + patterns('',
    url(r'^admin/', include(admin.site.urls)),
    #(r'^', include('haystack.urls')),
)
