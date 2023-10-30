from django.urls import path
from .views import *
#
urlpatterns = [
    path('', index),
    path('coupons/', coupons),
    path('coupons/<market_name>/', coupons_filter_market),
    # path('coupons/<market_name>/', coupons_filter_content),
]
#
#
