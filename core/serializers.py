from rest_framework import serializers
from .models import Students,Teacher,Subject


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ["id", "student_name", "roll_number", "date_of_birth", "gender"]

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["id","teacher_name","email","phone","hire_date"]

class SubjectSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id","subject_name","subject_code"]



class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = "__all__"
