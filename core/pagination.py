from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

class StudentPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 500
    limit_query_param = "limit"
    offset_query_param = "offset"
    page_size = 100               # default
    page_size_query_param = "page_size"
    max_page_size = 500           # max limit

    def get_limit(self, request):
        limit = request.query_params.get(self.limit_query_param)

        if limit is None:
            return self.default_limit

        try:
            limit = int(limit)
        except (TypeError, ValueError):
            raise ValidationError({"limit": "limit must be an integer"})

        if limit <= 0:
            raise ValidationError({"limit": "limit must be greater than 0"})

        if limit > self.max_limit:
            return self.max_limit

        return limit

    def get_offset(self, request):
        offset = request.query_params.get(self.offset_query_param, 0)

        try:
            offset = int(offset)
        except (TypeError, ValueError):
            raise ValidationError({"offset": "offset must be an integer"})

        if offset < 0:
            raise ValidationError({"offset": "offset cannot be negative"})

        return offset

    
    def get_paginated_response(self, data):
        return Response({
            "message": "Students fetched successfully",
            "total_count": self.page.paginator.count,
            "page": self.page.number,
            "page_size": self.page_size,
            "total_pages": self.page.paginator.num_pages,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "data": data,
        })
    
class Teacher_pagination(LimitOffsetPagination):
    default_limit = 50
    max_limit = 100

    limit_query_param = "limit"
    offset_query_param = "offset"

    def get_limit(self, request):
        
        limit = request.query_params.get(self.limit_query_param)

        if limit is None:
            return self.default_limit

        try:
            limit = int(limit)
        except (TypeError, ValueError):
            raise ValidationError({"limit": "limit must be an integer"})

        if limit <= 0:
            raise ValidationError({"limit": "limit must be greater than 0"})

        if limit > self.max_limit:
            return self.max_limit

        return limit
    def get_offset(self, request):
        offset = request.query_params.get(self.offset_query_param, 0)

        try:
            offset = int(offset)
        except (TypeError, ValueError):
            raise ValidationError({"offset": "offset must be an integer"})

        if offset < 0:
            raise ValidationError({"offset": "offset cannot be negative"})

        return offset

    def get_paginated_response(self, data):
        from rest_framework.response import Response

        return Response({
            "message": "Teachers fetched successfully",
            "total_count": self.count,
            "limit": self.limit,
            "offset": self.offset,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "data": data,
        })
        
