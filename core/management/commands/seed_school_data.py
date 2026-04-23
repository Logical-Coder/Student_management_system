import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import (
    Classroom,
    Subject,
    Teacher,
    Students,
    ClassSubject,
    TeacherClassSubject,
)


class Command(BaseCommand):
    help = "Seed large school data into database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--students",
            type=int,
            default=100000,
            help="Number of students to create",
        )
        parser.add_argument(
            "--teachers",
            type=int,
            default=500,
            help="Number of teachers to create",
        )

    def handle(self, *args, **options):
        student_count = options["students"]
        teacher_count = options["teachers"]

        self.stdout.write(self.style.WARNING("Seeding started..."))

        with transaction.atomic():
            self.create_subjects()
            self.create_classes()
            self.create_teachers(teacher_count)
            self.map_class_subjects()
            self.map_teacher_class_subjects()
            self.create_students(student_count)

        self.stdout.write(self.style.SUCCESS("Seeding completed successfully."))

    def create_subjects(self):
        if Subject.objects.exists():
            self.stdout.write("Subjects already exist, skipping...")
            return

        subject_data = [
            ("Mathematics", "MATH"),
            ("Science", "SCI"),
            ("English", "ENG"),
            ("Social Studies", "SOC"),
            ("Computer Science", "CS"),
            ("Physics", "PHY"),
            ("Chemistry", "CHE"),
            ("Biology", "BIO"),
            ("Kannada", "KAN"),
            ("Hindi", "HIN"),
        ]

        subjects = [
            Subject(subject_name=name, subject_code=code)
            for name, code in subject_data
        ]
        Subject.objects.bulk_create(subjects, batch_size=1000)
        self.stdout.write(self.style.SUCCESS("Subjects created."))

    def create_classes(self):
        if Classroom.objects.exists():
            self.stdout.write("Classes already exist, skipping...")
            return

        academic_year = "2026-2027"
        sections = ["A", "B", "C", "D"]

        class_rooms = []
        room_no = 100

        for class_no in range(1, 13):
            for section in sections:
                class_rooms.append(
                    Classroom(
                        class_name=str(class_no),
                        section=section,
                        room_number=str(room_no),
                        academic_year=academic_year,
                    )
                )
                room_no += 1

        Classroom.objects.bulk_create(class_rooms, batch_size=1000)
        self.stdout.write(self.style.SUCCESS("Classes created."))

    def create_teachers(self, teacher_count):
        if Teacher.objects.exists():
            self.stdout.write("Teachers already exist, skipping...")
            return

        teachers = []
        for i in range(1, teacher_count + 1):
            teachers.append(
                Teacher(
                    teacher_name=f"Teacher {i}",
                    email=f"teacher{i}@school.com",
                    phone=f"900000{i % 100000:05d}",
                    hire_date=date.today() - timedelta(days=random.randint(100, 3000)),
                )
            )

        Teacher.objects.bulk_create(teachers, batch_size=5000)
        self.stdout.write(self.style.SUCCESS(f"{teacher_count} teachers created."))

    def map_class_subjects(self):
        if ClassSubject.objects.exists():
            self.stdout.write("ClassSubject mappings already exist, skipping...")
            return

        classes = list(Classroom.objects.all())
        subjects = list(Subject.objects.all())

        mappings = []
        for class_room in classes:
            selected_subjects = random.sample(subjects, k=min(6, len(subjects)))
            for subject in selected_subjects:
                mappings.append(
                    ClassSubject(
                        class_room=class_room,
                        subject=subject,
                    )
                )

        ClassSubject.objects.bulk_create(mappings, batch_size=5000, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS("ClassSubject mappings created."))

    def map_teacher_class_subjects(self):
        if TeacherClassSubject.objects.exists():
            self.stdout.write("TeacherClassSubject mappings already exist, skipping...")
            return

        teachers = list(Teacher.objects.all())
        class_subjects = list(ClassSubject.objects.select_related("class_room", "subject"))

        mappings = []
        for cs in class_subjects:
            teacher = random.choice(teachers)
            mappings.append(
                TeacherClassSubject(
                    teacher=teacher,
                    class_room=cs.class_room,
                    subject=cs.subject,
                )
            )

        TeacherClassSubject.objects.bulk_create(
            mappings,
            batch_size=5000,
            ignore_conflicts=True,
        )
        self.stdout.write(self.style.SUCCESS("TeacherClassSubject mappings created."))

    def create_students(self, student_count):
        if Students.objects.exists():
            self.stdout.write("Students already exist, skipping...")
            return

        classes = list(Classroom.objects.all())
        genders = ["male", "female", "other"]

        students = []
        base_date = date(2005, 1, 1)

        for i in range(1, student_count + 1):
            dob = base_date + timedelta(days=random.randint(0, 5000))
            students.append(
                Students(
                    student_name=f"Student {i}",
                    roll_number=f"ROLL{i:06d}",
                    date_of_birth=dob,
                    gender=random.choice(genders),
                    class_room=random.choice(classes),
                )
            )

            if len(students) >= 5000:
                Students.objects.bulk_create(students, batch_size=5000)
                students = []
                self.stdout.write(f"Inserted {i} students...")

        if students:
            Students.objects.bulk_create(students, batch_size=5000)

        self.stdout.write(self.style.SUCCESS(f"{student_count} students created."))