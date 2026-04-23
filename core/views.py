from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from .models import Students,Teacher,Subject
from .serializers import StudentSerializer,TeacherSerializer,SubjectSerilizer
from .pagination import Teacher_pagination
from .paginationpage import StudentPagination
import time
from django.db import connection

import pdb

class StudentListCreateAPIView(ListCreateAPIView):
    queryset = Students.objects.all().order_by("id")
    serializer_class = StudentSerializer
    pagination_class = StudentPagination

    def get_queryset(self):
        pdb.set_trace() 
        queryset = Students.objects.all().order_by("id")

        student_name = self.request.query_params.get("student_name")
        gender = self.request.query_params.get("gender")

        if student_name:
            queryset = queryset.filter(student_name__icontains=student_name)

        if gender:
            queryset = queryset.filter(gender=gender)

        return queryset
    
    def list(self, request, *args, **kwargs):
        start_time = time.perf_counter()

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)

            end_time = time.perf_counter()
            response.data["benchmark"] = {
                "query_count": len(connection.queries),
                "response_time_ms": round((end_time - start_time) * 1000, 3),
                "strategy": "drf_limit_offset_pagination",
            }
            return response

        serializer = self.get_serializer(queryset, many=True)
        end_time = time.perf_counter()

        return Response({
            "message": "Students fetched successfully",
            "data": serializer.data,
            "benchmark": {
                "query_count": len(connection.queries),
                "response_time_ms": round((end_time - start_time) * 1000, 3),
                "strategy": "drf_no_pagination",
            }
        })

class TeacherListAPIView(ListAPIView):
    serializer_class = TeacherSerializer
    pagination_class = Teacher_pagination

    def get_queryset(self):
        queryset = Teacher.objects.all().order_by("id")

        teacher_name = self.request.query_params.get("teacher_name")

        if teacher_name:
            queryset = queryset.filter(teacher_name__icontains=teacher_name)

        return queryset 

        

class SubjectListAPIView(ListAPIView):
    serializer_class = SubjectSerilizer

    def get_queryset(self):
        
        queryset = Subject.objects.all().order_by("id")
        subject_name = self.request.query_params.get("subject_name")

        if subject_name:
            queryset = queryset.filter(subject_name__icontains=teacher_name)
        return queryset 




    


