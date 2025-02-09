import pytest
from django.contrib.contenttypes.models import ContentType
from django.test import Client
from django.urls import reverse

from accounts.models import User
from courses.models import Course, Enrollment, Subject
from lessons.models import Lesson, Module, Text


@pytest.mark.django_db
def test_lesson_detail_view_access():
    """Test accessing a lesson detail view."""
    client = Client()
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="password"
    )
    subject = Subject.objects.create(title="Test Subject", slug="test-subject")
    course = Course.objects.create(
        title="Test Course",
        subject=subject,
        slug="test-course",
        created_by=user,
        state=True,
    )
    module = Module.objects.create(
        course=course, title="Test Module", created_by=user
    )
    text_item = Text.objects.create(
        created_by=user, title="Text Item", content="Some content"
    )
    lesson_type = ContentType.objects.get_for_model(Text)
    lesson = Lesson.objects.create(
        title="Test Lesson",
        module=module,
        lesson_type=lesson_type,
        object_id=text_item.id,
        created_by=user,
        state=True,
    )
    Enrollment.objects.create(
        user=user, course=course, state=True, created_by=user
    )

    client.login(username="testuser", password="password")
    url = reverse("lessons", kwargs={"pk": lesson.id})

    response = client.get(url)
    assert response.status_code == 200
    assert "Some content" in response.content.decode()


@pytest.mark.django_db
def test_lesson_detail_view_permission_denied():
    """Test permission denied for inactive lesson or course."""
    client = Client()
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="password"
    )
    subject = Subject.objects.create(title="Test Subject", slug="test-subject")
    course = Course.objects.create(
        title="Test Course",
        subject=subject,
        slug="test-course",
        created_by=user,
        state=False,
    )
    module = Module.objects.create(
        course=course, title="Test Module", created_by=user
    )
    text_item = Text.objects.create(
        created_by=user, title="Text Item", content="Some content"
    )
    lesson_type = ContentType.objects.get_for_model(Text)
    lesson = Lesson.objects.create(
        title="Test Lesson",
        module=module,
        lesson_type=lesson_type,
        object_id=text_item.id,
        created_by=user,
        state=False,
    )

    client.login(username="testuser", password="password")
    url = reverse("lessons", kwargs={"pk": lesson.id})
    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_lesson_detail_view_redirect_not_enrolled():
    """Test redirect to course detail view if user is not enrolled."""
    client = Client()
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="password"
    )
    subject = Subject.objects.create(title="Test Subject", slug="test-subject")
    course = Course.objects.create(
        title="Test Course",
        subject=subject,
        slug="test-course",
        created_by=user,
        state=True,
    )
    module = Module.objects.create(
        course=course, title="Test Module", created_by=user
    )
    text_item = Text.objects.create(
        created_by=user, title="Text Item", content="Some content"
    )
    lesson_type = ContentType.objects.get_for_model(Text)
    lesson = Lesson.objects.create(
        title="Test Lesson",
        module=module,
        lesson_type=lesson_type,
        object_id=text_item.id,
        created_by=user,
        state=True,
    )

    client.login(username="testuser", password="password")
    url = reverse("lessons", kwargs={"pk": lesson.id})
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse("courses", kwargs={"slug": course.slug})
