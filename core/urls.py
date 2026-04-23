from django.urls import path
from .views import TeacherListAPIView,SubjectListAPIView,StudentListCreateAPIView


urlpatterns = [
    path("students/", StudentListCreateAPIView.as_view()),
    path("teachers/", TeacherListAPIView.as_view(), name="teachers-list"),
    path("subjects/", SubjectListAPIView.as_view(), name="teachers-list"),
]