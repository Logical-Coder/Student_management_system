from django.urls import path
from .views import TeacherListAPIView,SubjectListAPIView,StudentListCreateAPIView
from .views import students_n_plus_one_api,students_select_related_api,students_prefetch_related_api


urlpatterns = [
    path("students/", StudentListCreateAPIView.as_view()),
    path("teachers/", TeacherListAPIView.as_view(), name="teachers-list"),
    path("subjects/", SubjectListAPIView.as_view(), name="teachers-list"),
      path("students/n-plus-one/", students_n_plus_one_api, name="students-n-plus-one"),
    path("students/select-related/", students_select_related_api, name="students-select-related"),
    path("students/prefetch-related/", students_prefetch_related_api, name="students-prefetch-related"),
]