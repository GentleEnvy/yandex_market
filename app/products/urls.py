from django.urls import path

from .views import *
from .views.plot import ProductsPlotView

urlpatterns = [
    path('', ProductsView.as_view()),
    path('changes/', ProductsChangesView.as_view()),
    path('<int:id>/', ProductView.as_view()),
    path('<int:id>/prices/', ProductPricesView.as_view()),
    path('<int:id>/plot/', ProductsPlotView.as_view())
]
