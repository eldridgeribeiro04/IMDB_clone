from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class WatchListPagination(PageNumberPagination):
    page_size = 10
    # page_query_param = "p"
    last_page_strings = "end"
    
    
class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 5