from rest_framework import pagination


class PostPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page_number'


class CommentPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page_number'
