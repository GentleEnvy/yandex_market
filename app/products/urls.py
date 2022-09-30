from django.urls import path

from .views import *

urlpatterns = [
    path('', ProductsView.as_view()),
    path('<int:id>/prices/', ProductPricesView.as_view())
]
