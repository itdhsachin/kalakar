"""Test fixtures for the accounts, courses, lessons, and modules apps.

This module contains pytest fixtures for creating test data for the accounts,
courses, lessons, and modules applications.
"""

import pytest
from django.contrib.contenttypes.models import ContentType

from accounts.models import User
from courses.models import Course, Subject
from lessons.models import File, Image, Lesson, Text, Video
from modules.models import Module


@pytest.fixture
def user():
    """Create a test user.

    Returns:
        User: The created test user.
    """
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="password"
    )


@pytest.fixture
def subject():
    """Create a test subject.

    Returns:
        Subject: The created test subject.
    """
    return Subject.objects.create(title="Test Subject", slug="test-subject")


@pytest.fixture
def course(user, subject):
    """Create a test course.

    Args:
        user (User): The user who creates the course.
        subject (Subject): The subject of the course.

    Returns:
        Course: The created test course.
    """
    return Course.objects.create(
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


@pytest.fixture
def module(course, user):
    """Create a test module.

    Args:
        course (Course): The course to which the module belongs.
        user (User): The user who creates the module.

    Returns:
        Module: The created test module.
    """
    return Module.objects.create(
        course=course, title="Test Module", created_by=user
    )


@pytest.fixture
def text_item(user):
    """Create a test text item.

    Args:
        user (User): The user who creates the text item.

    Returns:
        Text: The created test text item.
    """
    return Text.objects.create(
        created_by=user, title="Text Item", content="Some content"
    )


@pytest.fixture
def file_item(user):
    """Create a test file item.

    Args:
        user (User): The user who creates the file item.

    Returns:
        File: The created test file item.
    """
    return File.objects.create(
        created_by=user, title="File Item", file="path/to/file"
    )


@pytest.fixture
def image_item(user):
    """Create a test image item.

    Args:
        user (User): The user who creates the image item.

    Returns:
        Image: The created test image item.
    """
    return Image.objects.create(
        created_by=user, title="Image Item", image="path/to/image"
    )


@pytest.fixture
def video_item(user):
    """Create a test video item.

    Args:
        user (User): The user who creates the video item.

    Returns:
        Video: The created test video item.
    """
    return Video.objects.create(
        created_by=user, title="Video Item", url="https://www.example.com"
    )


@pytest.fixture
def lesson(module, user, text_item):
    """Create a test lesson.

    Args:
        module (Module): The module to which the lesson belongs.
        user (User): The user who creates the lesson.
        text_item (Text): The text item associated with the lesson.

    Returns:
        Lesson: The created test lesson.
    """
    lesson_type = ContentType.objects.get_for_model(Text)
    return Lesson.objects.create(
        title="Test Lesson",
        module=module,
        lesson_type=lesson_type,
        object_id=text_item.id,
        created_by=user,
        state=True,
    )
