from django.db import models

# Create your models here.

class TimeStampedModel(models.Model):

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True





class Classroom(TimeStampedModel):
    class_name = models.CharField(max_length=50)
    section = models.CharField(max_length=50,blank=True,null=True)
    room_number = models.CharField(max_length=20,blank=True,null=True)
    academic_year = models.CharField(max_length=20,blank=True,null=True)

    class Meta:
        db_table = "classes"
        ordering = ["class_name","section"]
        unique_together = ("class_name","section","academic_year")
    
    def __str__(self):
        if self.section:
            return f"{self.class_name}---{self.section}"
        return self.class_name
        

class Subject(TimeStampedModel):
    subject_name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "subjects"
        ordering = ["subject_name"]

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"
    

class Teacher(TimeStampedModel):
    teacher_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    hire_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "teachers"
        ordering = ["teacher_name"]

    def __str__(self):
        return self.teacher_name


class Students(TimeStampedModel):
    GENDER_CHOICES = (
        ('male',"Male"),
        ('female','Female'),
        ('other','Other')

    )
    student_name = models.CharField(max_length=100,db_index=True)
    roll_number = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField(blank=True,null=True)
    gender = models.CharField(max_length=20,choices=GENDER_CHOICES,blank=False,null=False)
    class_room = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name="Students"
    )
    class Meta:
        db_table = "students"
        ordering = ["student_name"]

    def __str__(self):
        return f"{self.student_name} - {self.roll_number}"


class ClassSubject(TimeStampedModel):
    class_room = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name="class_subjects",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="subject_classes",
    )

    class Meta:
        db_table = "class_subjects"
        unique_together = ("class_room", "subject")
        ordering = ["class_room", "subject"]

    def __str__(self):
        return f"{self.class_room} - {self.subject}"
    
class TeacherClassSubject(TimeStampedModel):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="teacher_class_subjects",
    )
    class_room = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name="teacher_class_subjects",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="teacher_class_subjects",
    )

    class Meta:
        db_table = "teacher_class_subject"
        unique_together = ("teacher", "class_room", "subject")
        ordering = ["teacher", "class_room", "subject"]

    def __str__(self):
        return f"{self.teacher} teaches {self.subject} for {self.class_room}"

