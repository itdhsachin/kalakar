"""View module."""

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView

from courses.models import Course, Enrollment
from lessons.models import Lesson
from students.forms import CourseEnrollForm


class StudentRegistrationView(CreateView):
    """View to handle student registration process.

    Attributes:
        template_name (str): The template to render the registration page.
        form_class (class): The form class used for creating a new user.
        success_url (str): URL to redirect after successful registration.

    Methods:
        form_valid(form): Handles the authentication and login of the user after successful registration.
    """

    template_name = "students/student/registration.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("student_course_list")

    def form_valid(self, form):
        """Handles the authentication and login of the user after successful registration.

        Args:
            form (Form): The form containing user registration data.

        Returns:
            HttpResponse: The HTTP response after processing the form.
        """
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd["username"], password=cd["password1"])
        login(self.request, user)
        return result


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    """View to handle student course enrollment process.

    Attributes:
        course (Course): The course to enroll in.
        form_class (class): The form class used for course enrollment.

    Methods:
        form_valid(form): Enrolls the student in the selected course.
        get_success_url(): Returns the URL to redirect after successful enrollment.
    """

    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        """Enrolls the student in the selected course.

        Args:
            form (Form): The form containing course enrollment data.

        Returns:
            HttpResponse: The HTTP response after processing the form.
        """
        self.course = form.cleaned_data["course"]
        user = self.request.user

        # Check if the enrollment already exists
        _, created = Enrollment.objects.get_or_create(
            user=user, course=self.course, defaults={"created_by": user}
        )

        if not created:
            # Enrollment already exists
            form.add_error(None, "You are already enrolled in this course.")
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        """Returns the URL to redirect after successful enrollment.

        Returns:
            str: The URL to redirect.
        """
        return reverse_lazy("student_course_detail", args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    """View to display the list of courses a student is enrolled in.

    Attributes:
        model (class): The model representing a course.
        template_name (str): The template to render the list of courses.

    Methods:
        get_queryset(): Returns the queryset of courses the student is enrolled in.
    """

    model = Course
    template_name = "students/student/list.html"

    def get_queryset(self):
        """Returns the queryset of courses the student is enrolled in.

        Returns:
            QuerySet: The queryset of courses.
        """
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(DetailView):
    """View to display the details of a course a student is enrolled in.

    Attributes:
        model (class): The model representing a course.
        template_name (str): The template to render the course details.

    Methods:
        get_queryset(): Returns the queryset of courses the student is enrolled in.
        get_context_data(**kwargs): Adds additional context data for the template.
    """

    model = Course
    template_name = "students/student/detail.html"

    def get_queryset(self):
        """Returns the queryset of courses the student is enrolled in.

        Returns:
            QuerySet: The queryset of courses.
        """
        qs = super().get_queryset()
        return qs.filter(enrollments__user=self.request.user)

    def get_context_data(self, **kwargs):
        """Adds additional context data for the template.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The context data for the template.
        """
        context = super().get_context_data(**kwargs)
        course = self.get_object()

        # Fetch modules and attach lessons to each module
        modules = course.modules.all()
        for module in modules:
            module.lessons.set(Lesson.objects.filter(module=module))

        # Attach modules to course object
        course.modules.set(modules)

        context["course"] = course

        if "module_id" in self.kwargs:
            context["module"] = course.modules.get(id=self.kwargs["module_id"])
        else:
            modules_list = list(course.modules.all())
            if modules_list:
                context["module"] = modules_list[0]

        return context
