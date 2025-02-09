import pytest

from courses.models import Course


@pytest.mark.django_db
def test_create_course(course):
    """Test creating a Course."""
    assert course.title == "Test Course"
    assert course.subject.title == "Test Subject"
    assert course.slug == "test-course"
    assert course.description == "This is a test course."
    assert course.price == 100.00
    assert course.currency == "USD"
    assert course.is_paid is True
    assert course.created_by.username == "testuser"
    assert course.state is True


@pytest.mark.django_db
def test_course_str(course):
    """Test the string representation of a Course."""
    assert str(course) == "Test Course"


@pytest.mark.django_db
def test_course_ordering(user, subject):
    """Test the ordering of Courses."""
    course1 = Course.objects.create(
        title="Course 1", subject=subject, slug="course-1", created_by=user
    )
    course2 = Course.objects.create(
        title="Course 2", subject=subject, slug="course-2", created_by=user
    )
    courses = Course.objects.all()
    assert list(courses) == [course2, course1]


@pytest.mark.django_db
def test_course_is_free(user, subject):
    """Test creating a free Course."""
    course = Course.objects.create(
        title="Free Course",
        subject=subject,
        slug="free-course",
        description="This is a free course.",
        price=0.00,
        currency="",
        is_paid=False,
        enroll_start_date=None,
        enroll_end_date=None,
        completion_days=30,
        created_by=user,
        state=True,
    )
    assert course.title == "Free Course"
    assert course.subject.title == "Test Subject"
    assert course.slug == "free-course"
    assert course.description == "This is a free course."
    assert course.price == 0.00
    assert course.currency == ""
    assert course.is_paid is False
    assert course.created_by.username == "testuser"
    assert course.state is True
