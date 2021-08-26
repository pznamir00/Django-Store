from rest_framework.pagination import LimitOffsetPagination


class ProductPagination(LimitOffsetPagination):
    default_limit = 30
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 80