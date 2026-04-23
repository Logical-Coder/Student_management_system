from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.apps import AppConfig


class StudentPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 500

    def get_page_size(self, request):
        page_size = request.query_params.get(self.page_size_query_param)

        if page_size is None:
            return self.page_size

        try:
            page_size = int(page_size)
        except (TypeError, ValueError):
            raise ValidationError({"page_size": "page_size must be an integer"})

        if page_size <= 0:
            raise ValidationError({"page_size": "page_size must be greater than 0"})

        if page_size > self.max_page_size:
            return self.max_page_size

        return page_size

    def get_paginated_response(self, data):
        return Response({
            "message": "Students fetched successfully",
            "total_count": self.page.paginator.count,
            "page": self.page.number,
            "page_size": self.get_page_size(self.request),
            "total_pages": self.page.paginator.num_pages,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "data": data,
        })