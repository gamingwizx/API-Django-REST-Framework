from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination,CursorPagination

class newPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'p'
    page_size_query_param = 'size'
    last_page_strings = ['end']

class offsetPagination(LimitOffsetPagination):
    default_limit = 2
    limit_query_param = 'max'
    offset_query_param = 'start'

class cursorPagination(CursorPagination):
    page_size = 2
    ordering = 'id'