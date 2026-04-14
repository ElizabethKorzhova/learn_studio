from django.db.models.signals import post_save
from django.dispatch import receiver
from ls.models import Homework, Enrollment, Notification, HomeworkSubmission


@receiver(post_save, sender=Homework)
def notify_new_homework(sender, instance, created, **kwargs):
    """Notify new homework
    """
    if not created:
        return

    course = instance.lesson.course
    students = Enrollment.objects.filter(course=course).values_list("user", flat=True)

    notifications = [
        Notification(
            user_id=user_id,
            title="New homework assigned",
            message=f"{instance.title}",
            type="homework",
            related_id=instance.id
        )
        for user_id in students
    ]

    Notification.objects.bulk_create(notifications)


@receiver(post_save, sender=HomeworkSubmission)
def notify_grade(sender, instance, created, **kwargs):
    """Notify new homework submission
    """
    if created:
        return

    if instance.score is None:
        return

    Notification.objects.create(
        user=instance.user,
        title="Homework graded",
        message=f"Score: {instance.score}",
        type="grade",
        related_id=instance.id
    )
