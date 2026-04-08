from rest_framework import serializers

from ls import models


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SocialLink
        fields = ["platform_name", "url"]


class UserSerializer(serializers.ModelSerializer):
    social_links = SocialLinkSerializer(many=True, read_only=True)

    class Meta:
        model = models.User
        fields = ["id", "username", "email", "first_name", "last_name", "social_links"]
        read_only_fields = fields


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["id", "first_name", "last_name"]
        read_only_fields = fields


class MyProfileSerializer(serializers.ModelSerializer):
    social_links = SocialLinkSerializer(many=True, read_only=True)

    class Meta:
        model = models.User
        fields = ["id", "username", "email", "first_name", "last_name", "social_links"]
        read_only_fields = ["id", "role"]


class LessonShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = ["id", "title", "order_index"]


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = ["id", "title", "content", "order_index", "images"]
        read_only_fields = ["id"]


class HomeworkSerializer(serializers.ModelSerializer):
    created_by = UserShortSerializer(read_only=True)

    class Meta:
        model = models.Homework
        fields = ["id", "title", "task", "deadline", "complexity", "deadline_date", "created_by"]
        read_only_fields = ["id", "created_by"]


class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    is_enrolled = serializers.SerializerMethodField()
    user_stats = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = [
            "id", "is_enrolled", "title", "description", "price",
            "start_at", "duration", "created_at", 'user_stats', "instructor"
        ]
        read_only_fields = ["id", "created_at"]

    def get_is_enrolled(self, obj):
        request = self.context.get("request")
        return models.Enrollment.objects.filter(user=request.user, course=obj).exists()

    def get_user_stats(self, obj):
        request = self.context.get("request")
        last_enrollment = models.Enrollment.objects.filter(user=request.user, course=obj).last()
        if last_enrollment:
            return EnrollmentSerializer(last_enrollment, many=False, read_only=True).data
        return None


class CourseDetailSerializer(CourseSerializer):
    lessons = LessonShortSerializer(many=True, read_only=True)

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ["lessons"]


class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = models.Enrollment
        fields = ["id", "user", "course", "course_title", "user_email", "enrolled_at", "user_progress",
                  "attendance", "updated_at"]
        read_only_fields = ["id", "user", "enrolled_at", "updated_at"]


class ParticipantSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = models.Enrollment
        fields = ['user']


class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    homework_title = serializers.CharField(source="homework.title", read_only=True)

    class Meta:
        model = models.HomeworkSubmission
        fields = [
            "id", "user", "user_email", "homework", "homework_title",
            "messages", "files", "url", "submitted_at", "score"
        ]
        read_only_fields = ["id", "user", "submitted_at", "score"]
