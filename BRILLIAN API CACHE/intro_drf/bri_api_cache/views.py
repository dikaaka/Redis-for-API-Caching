from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.core.cache import cache
from .serializers import *
from django.views.decorators.cache import cache_page
from django.db.models import Q

# Create your views here.
class InstitutionsView(ListAPIView):
    queryset = Institutions.objects.all()
    serializer_class = InstitutionsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        institution_name = self.request.query_params.get('name', None)
        net_transactions_filter = self.request.query_params.get('net_transaction', None)

        if institution_name:
            queryset = queryset.filter(
                Q(top_sellers__contains=[{'name': institution_name}]) |
                Q(top_buyers__contain=[{'name': institution_name}]))
        if net_transactions_filter == 'negative':
            queryset = queryset.filter(net_transaction__lt=0)
        if net_transactions_filter == 'positive':
            queryset = queryset.filter(net_transaction__gt=0)
        return queryset
    
    def list(self, request):
        query_params = request.query_params.urlencode()
        cache_key = f'institution-trade-{query_params}'  # Define a unique cache key for this data
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
    
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset()  # Query the database for the data
            print(result.values())  # Log the retrieved data (for debugging purposes)
            
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
            
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
        
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)
        print(result.data)  # Log the serialized data (for debugging purposes)

        return Response(result.data)  # Return the serialized data as a response
    
class ReportsView(ListAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        reports_name = self.request.query_params.get('sub_sector', None)
        revenue_growth = self.request.query_params.get('avg_yoy_q_revenue_growth', None)
        earning_growth = self.request.query_params.get('avg_yoy_q_earnings_growth', None)
        if reports_name:
            queryset = queryset.filter(sub_sector__contains=reports_name)
        if revenue_growth == 'negative':
            queryset = queryset.filter(avg_yoy_q_revenue_growth__lt=0)
        if revenue_growth == 'positive':
            queryset = queryset.filter(avg_yoy_q_revenue_growth__gt=0)
        if earning_growth == 'negative':
            queryset = queryset.filter(avg_yoy_q_earnings_growth__lt=0)
        if earning_growth == 'positive':
            queryset = queryset.filter(avg_yoy_q_earnings_growth__gt=0)
        return queryset
    
    def list(self, request):
        query_params = request.query_params.urlencode()
        cache_key = f'get-reports-trade-{query_params}'
        result = cache.get(cache_key)

        if not result:
            print('Hitting DB')
            result = self.get_queryset()
            print(result.values())
            cache.set(cache_key, result, 60)
        else:
            print('Cache Retrieved!')
        result = self.serializer_class(result, many=True)
        print(result.data)
        return Response(result.data)
    
class MetadataView(ListAPIView):
    queryset = Metadata.objects.all()
    serializer_class = MetadataSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        sector_name = self.request.query_params.get('sector', None)
        sub_sector_name = self.request.query_params.get('sub_sector', None)
        if sector_name:
            queryset = queryset.filter(sector__contains=sector_name)
        if sub_sector_name:
            queryset = queryset.filter(sub_sector__contains=sub_sector_name)
        return queryset
    
    def list(self, request):
        query_params = request.query_params.urlencode()
        cache_key = f'get-metadata-sector-{query_params}'
        result = cache.get(cache_key)

        if not result:
            print('Hitting DB')
            result = self.get_queryset()
            print(result.values())
            cache.set(cache_key, result, 60)
        else:
            print('Cache Retrieved!')
        result = self.serializer_class(result, many=True)
        print(result.data)
        return Response(result.data)


