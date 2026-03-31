import random
import time

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from faker import Faker

from ls.models import User, Course, Lesson, Homework, SocialLink, Enrollment, HomeworkSubmission


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--clear", type=bool, default=False)
        parser.add_argument("--users", type=int, default=10)
        parser.add_argument("--courses", type=int, default=2)
        parser.add_argument("--lessons", type=int, default=10)

    def handle(self, *args, **options):
        start_time = time.perf_counter()

        users_count = options["users"]
        courses_count = options["courses"]
        lessons_count = options["lessons"]

        if options["clear"]:
            self.stdout.write("Cleaning the database...")
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write("Database cleared.")

        self.stdout.write("Starting database seeding...")
        fake = Faker()
        instructors = []
        students = []

        if users_count > 0:
            users = self.create_users(users_count, fake)
            instructors = [user for user in users if user.role == "instructor"]
            students = [user for user in users if user.role == "student"]

        if courses_count > 0 and lessons_count > 0 and students and instructors:
            for _ in range(courses_count):
                self.create_course(instructors, students, lessons_count, fake)

        duration = time.perf_counter() - start_time
        self.stdout.write(f"Done. Command executed in {duration:.4f} seconds.")

    @staticmethod
    def create_users(count: int, fake: Faker):
        roles = "instructor", "student", "admin"
        social_platforms = "facebook", "x", "instagram", "youtube", "github", "linkedin"
        users = []
        for i in range(count):
            role = "instructor" if i == 1 else "student" if i == 2 else random.choice(roles)

            user = User.objects.create(
                username=fake.unique.user_name(),
                password=make_password(fake.password()),
                email=fake.unique.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=fake.msisdn(),
                role=role
            )

            social_links = [
                SocialLink(
                    user=user,
                    platform_name=random.choice(social_platforms),
                    url=fake.url(),
                ) for _ in range(random.randint(1, len(social_platforms)))
            ]

            SocialLink.objects.bulk_create(social_links)
            users.append(user)
        return users

    @staticmethod
    def create_course(instructors, students, lessons_count: int, fake: Faker):
        instructor = random.choice(instructors)
        enrolled_students = random.sample(students, random.randint(1, len(students)))

        course = Course.objects.create(
            instructor=instructor,
            title=fake.catch_phrase(),
            description=fake.text(),
            price=fake.pydecimal(min_value=0, max_value=10, right_digits=2),
            start_at=fake.date_time_between(start_date="-30d", end_date="+2m",
                                            tzinfo=timezone.get_current_timezone()),
            duration=random.randint(10, 40),
        )

        lessons_to_create = [
            Lesson(course=course, title=fake.sentence(),
                   content=fake.text(), order_index=i + 1)
            for i in range(lessons_count)
        ]
        lessons = Lesson.objects.bulk_create(lessons_to_create)

        homeworks_to_create = []
        for lesson in lessons:
            deadline = fake.date_time_between(start_date="+1d", end_date="+10d",
                                              tzinfo=timezone.get_current_timezone())
            homeworks_to_create.append(Homework(
                lesson=lesson,
                title=fake.sentence(),
                task=fake.text(),
                deadline=deadline,
                complexity=random.randint(1, 3),
                created_by=instructor,
                deadline_date=deadline.date()
            ))
        homeworks = Homework.objects.bulk_create(homeworks_to_create)

        submissions_to_create = []
        enrollments_to_create = []

        for enrolled_student in enrolled_students:
            submitted_count = 0
            for homework in homeworks:
                if random.choice([True, False]):
                    is_completed = random.choice([True, False])
                    submissions_to_create.append(HomeworkSubmission(
                        user=enrolled_student,
                        homework=homework,
                        messages={"message": fake.text(),
                                  "feedback": fake.text() if is_completed else ""},
                        score=random.randint(60, 100) if is_completed else None,
                    ))
                    submitted_count += 1

            progress = int((submitted_count / lessons_count) * 100) \
                if lessons_count > 0 else 0
            status = "completed" if progress >= 90 else "in progress" \
                if 90 > progress > 0 else "not started"

            enrollments_to_create.append(Enrollment(
                user=enrolled_student,
                course=course,
                course_status=status,
                user_progress=progress,
                attendance=round(random.uniform(0.0, 1.0), 2),
            ))

        HomeworkSubmission.objects.bulk_create(submissions_to_create)
        Enrollment.objects.bulk_create(enrollments_to_create)
