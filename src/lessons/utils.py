from datetime import date, timedelta
from courses.models import Enrollment


def can_access_lesson(user, lesson):

    enrollment = Enrollment.objects.filter(
        user=user,
        course=lesson.module.course
    ).first()

    if not enrollment:
        return False

    if not enrollment.batch:
        return False

    batch = enrollment.batch

    release_date = batch.start_date + timedelta(
        days=lesson.release_after_days
    )

    return date.today() >= release_date