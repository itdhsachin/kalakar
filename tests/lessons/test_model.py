import pytest
from django.contrib.contenttypes.models import ContentType

from accounts.models import User
from courses.models import Course, Subject
from lessons.models import File, Image, Lesson, Text, Video
from modules.models import Module


@pytest.mark.django_db
def test_create_lesson():
    """Test creating a Lesson."""
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
    module = Module.objects.create(
        course=course, title="Test Module", created_by=user
    )
    lesson_type = ContentType.objects.get_for_model(Text)
    lesson = Lesson.objects.create(
        title="Test Lesson",
        module=module,
        lesson_type=lesson_type,
        object_id=1,
        created_by=user,
    )
    assert lesson.title == "Test Lesson"
    assert lesson.module == module
    assert lesson.lesson_type == lesson_type
    assert lesson.created_by == user


@pytest.mark.django_db
def test_lesson_state():
    """Test the state of a Lesson."""
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
    module = Module.objects.create(
        course=course, title="Test Module", created_by=user
    )
    lesson_type = ContentType.objects.get_for_model(Text)
    lesson = Lesson.objects.create(
        title="Test Lesson",
        module=module,
        lesson_type=lesson_type,
        object_id=1,
        created_by=user,
        state=True,
    )
    assert lesson.state is True


@pytest.mark.django_db
def test_get_type():
    """Test the get_type method."""
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
    module = Module.objects.create(
        course=course, title="Test Module", created_by=user
    )
    lesson_type = ContentType.objects.get_for_model(Video)
    lesson = Lesson.objects.create(
        title="Test Lesson",
        module=module,
        lesson_type=lesson_type,
        object_id=1,
        created_by=user,
    )
    assert lesson.get_type() == "Video"


@pytest.mark.django_db
def test_create_different_lesson_types():
    """Test creating lessons with different item types."""
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
    module = Module.objects.create(
        course=course, title="Test Module", created_by=user
    )

    text_item = Text.objects.create(
        created_by=user, title="Text Item", content="Some content"
    )
    text_lesson = Lesson.objects.create(
        title="Text Lesson",
        module=module,
        lesson_type=ContentType.objects.get_for_model(Text),
        object_id=text_item.id,
        created_by=user,
    )
    assert text_lesson.item == text_item

    file_item = File.objects.create(
        created_by=user, title="File Item", file="path/to/file"
    )
    file_lesson = Lesson.objects.create(
        title="File Lesson",
        module=module,
        lesson_type=ContentType.objects.get_for_model(File),
        object_id=file_item.id,
        created_by=user,
    )
    assert file_lesson.item == file_item

    image_item = Image.objects.create(
        created_by=user, title="Image Item", image="path/to/image"
    )
    image_lesson = Lesson.objects.create(
        title="Image Lesson",
        module=module,
        lesson_type=ContentType.objects.get_for_model(Image),
        object_id=image_item.id,
        created_by=user,
    )
    assert image_lesson.item == image_item

    video_item = Video.objects.create(
        created_by=user, title="Video Item", url="https://www.example.com"
    )
    video_lesson = Lesson.objects.create(
        title="Video Lesson",
        module=module,
        lesson_type=ContentType.objects.get_for_model(Video),
        object_id=video_item.id,
        created_by=user,
    )
    assert video_lesson.item == video_item
