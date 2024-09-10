from .views import InstitutionsView, ReportsView, MetadataView
from django.urls import path, include

urlpatterns = [
    path('get-institution-trade', InstitutionsView.as_view(), name='get-institution-trade'),
    path('get-reports-trade', ReportsView.as_view(), name='get-reports-trade'),
    path('get-metadata-sector', MetadataView.as_view(), name='get-metadata-sector'),
]