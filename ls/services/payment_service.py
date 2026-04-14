from ls.models import Enrollment, Transaction


def confirm_payment(transaction: Transaction) -> None:
    """Confirms payment and enrolls user in course
    """
    if transaction.status == "success":
        return

    transaction.status = "success"
    transaction.save()

    Enrollment.objects.get_or_create(
        user=transaction.user,
        course=transaction.course
    )
