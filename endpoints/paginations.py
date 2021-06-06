from rest_framework import pagination

class LargeResultSetPagination(pagination.PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    page_size_query_description = 'large_result'
    max_page_size = 10000
    
    
class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    page_size_query_description = 'standard_result'
    max_page_size = 1000

class SmallResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_size_query_description = 'small_result'
    max_page_size = 100
    