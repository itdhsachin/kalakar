import pytest

from accounts.models import User
from courses.models import Course, Subject


@pytest.mark.django_db
def test_create_course():
    """Test creating a Course."""
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="password"
    )
    subject = Subject.objects.create(title="Test Subject", slug="test-subject")
    course = Course.objects.create(
        title="Test Course",
        subject=subject,
        slug="test-course",
        description="This is a test course.",
        price=100.00,
        currency="USD",
        is_paid=True,
        enroll_start_date=None,
        enroll_end_date=None,
        completion_days=30,
        created_by=user,
        state=True,
    )
    assert course.title == "Test Course"
    assert course.subject == subject
    assert course.slug == "test-course"
    assert course.description == "This is a test course."
    assert course.price == 100.00
    assert course.currency == "USD"
    assert course.is_paid is True
    assert course.created_by == user
    assert course.state is True


@pytest.mark.django_db
def test_course_str():
    """Test the string representation of a Course."""
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="password"
    )
    subject = Subject.objects.create(title="Test Subject", slug="test-subject")
    course = Course.objects.create(
        title="Test Course",
        subject=subject,
        slug="test-course",
        created_by=user,
    )
    assert str(course) == "Test Course"


@pytest.mark.django_db
def test_course_ordering():
    """Test the ordering of Courses."""
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="password"
    )
    subject = Subject.objects.create(title="Test Subject", slug="test-subject")
    course1 = Course.objects.create(
        title="Course 1", subject=subject, slug="course-1", created_by=user
    )
    course2 = Course.objects.create(
        title="Course 2", subject=subject, slug="course-2", created_by=user
    )
    courses = Course.objects.all()
    assert list(courses) == [course2, course1]


@pytest.mark.django_db
def test_course_is_free():
    """Test creating a free Course."""
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="password"
    )
    subject = Subject.objects.create(title="Test Subject", slug="test-subject")
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
    assert course.subject == subject
    assert course.slug == "free-course"
    assert course.description == "This is a free course."
    assert course.price == 0.00
    assert course.currency == ""
    assert course.is_paid is False
    assert course.created_by == user
    assert course.state is True
