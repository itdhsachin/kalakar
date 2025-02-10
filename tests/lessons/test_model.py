import pytest
from django.contrib.contenttypes.models import ContentType

from lessons.models import File, Image, Lesson, Text, Video


@pytest.mark.django_db
def test_create_lesson(module, user):
    """Test creating a Lesson."""
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
def test_lesson_state(lesson):
    """Test the state of a Lesson."""
    assert lesson.state is True


@pytest.mark.django_db
def test_get_type(module, user):
    """Test the get_type method."""
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
def test_create_different_lesson_types(
    module, user, text_item, file_item, image_item, video_item
):
    """Test creating lessons with different item types."""
    text_lesson = Lesson.objects.create(
        title="Text Lesson",
        module=module,
        lesson_type=ContentType.objects.get_for_model(Text),
        object_id=text_item.id,
        created_by=user,
    )
    assert text_lesson.item == text_item

    file_lesson = Lesson.objects.create(
        title="File Lesson",
        module=module,
        lesson_type=ContentType.objects.get_for_model(File),
        object_id=file_item.id,
        created_by=user,
    )
    assert file_lesson.item == file_item

    image_lesson = Lesson.objects.create(
        title="Image Lesson",
        module=module,
        lesson_type=ContentType.objects.get_for_model(Image),
        object_id=image_item.id,
        created_by=user,
    )
    assert image_lesson.item == image_item

    video_lesson = Lesson.objects.create(
        title="Video Lesson",
        module=module,
        lesson_type=ContentType.objects.get_for_model(Video),
        object_id=video_item.id,
        created_by=user,
    )
    assert video_lesson.item == video_item
