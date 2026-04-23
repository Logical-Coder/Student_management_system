from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from .models import Students,Teacher,Subject
from .serializers import StudentSerializer,TeacherSerializer,SubjectSerilizer
from .pagination import Teacher_pagination
from .paginationpage import StudentPagination
import time
from django.db import connection


import time
from django.conf import settings
from django.db import connection, reset_queries
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Students


@require_GET
def students_n_plus_one_api(request):
    if settings.DEBUG:
        reset_queries()

    start_time = time.perf_counter()

    limit = int(request.GET.get("limit", 100))
    offset = int(request.GET.get("offset", 0))

    students = Students.objects.all().order_by("id")[offset:offset + limit]

    data = []
    for student in students:
        data.append({
            "id": student.id,
            "student_name": student.student_name,
            "roll_number": student.roll_number,
            "gender": student.gender,
            "class_room_id": student.class_room.id,
            "class_name": student.class_room.class_name,
            "section": student.class_room.section,
        })

    end_time = time.perf_counter()

    query_count = len(connection.queries) if settings.DEBUG else 0

    return JsonResponse({
        "message": "N+1 problem created intentionally",
        "strategy": "plain queryset with related object access inside loop",
        "total_returned": len(data),
        "query_count": query_count,
        "response_time_ms": round((end_time - start_time) * 1000, 3),
        "data": data,
    })


@require_GET
def students_select_related_api(request):
    if settings.DEBUG:
        reset_queries()

    start_time = time.perf_counter()

    limit = int(request.GET.get("limit", 100))
    offset = int(request.GET.get("offset", 0))

    students = (
        Students.objects
        .select_related("class_room")
        .all()
        .order_by("id")[offset:offset + limit]
    )

    data = []
    for student in students:
        data.append({
            "id": student.id,
            "student_name": student.student_name,
            "roll_number": student.roll_number,
            "gender": student.gender,
            "class_room_id": student.class_room.id,
            "class_name": student.class_room.class_name,
            "section": student.class_room.section,
        })

    end_time = time.perf_counter()

    query_count = len(connection.queries) if settings.DEBUG else 0

    return JsonResponse({
        "message": "N+1 solved using select_related",
        "strategy": "select_related(class_room)",
        "total_returned": len(data),
        "query_count": query_count,
        "response_time_ms": round((end_time - start_time) * 1000, 3),
        "data": data,
    })

@require_GET
def students_prefetch_related_api(request):
    if settings.DEBUG:
        reset_queries()

    start_time = time.perf_counter()

    limit = int(request.GET.get("limit", 100))
    offset = int(request.GET.get("offset", 0))

    students = (
        Students.objects
        .prefetch_related("class_room")
        .all()
        .order_by("id")[offset:offset + limit]
    )

    data = []
    for student in students:
        data.append({
            "id": student.id,
            "student_name": student.student_name,
            "roll_number": student.roll_number,
            "gender": student.gender,
            "class_room_id": student.class_room.id,
            "class_name": student.class_room.class_name,
            "section": student.class_room.section,
        })

    end_time = time.perf_counter()

    query_count = len(connection.queries) if settings.DEBUG else 0

    return JsonResponse({
        "message": "N+1 reduced using prefetch_related",
        "strategy": "prefetch_related(class_room)",
        "total_returned": len(data),
        "query_count": query_count,
        "response_time_ms": round((end_time - start_time) * 1000, 3),
        "data": data,
    })
class StudentListCreateAPIView(ListCreateAPIView):
    queryset = Students.objects.all().order_by("id")
    serializer_class = StudentSerializer
    pagination_class = StudentPagination

    def get_queryset(self):
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






    


