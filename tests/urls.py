from django.conf.urls.defaults import *

from oscar.app import shop

urlpatterns = patterns('',
    (r'', include(shop.urls)),
)