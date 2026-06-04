"""Course view module."""

# from django.core.cache import cache   # the cache is stopped
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.apps import apps
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from django.views.generic.base import TemplateView
from courses.forms import ModuleFormSet
from courses.models import Course, Subject,Enrollment
from lessons.models import Lesson
from modules.models import Module
from students.forms import CourseEnrollForm
from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from coupon.models import Coupons

from django.db.models import Q, Count
from accounts.models import Student

class OwnerMixin:
    """Mixin to filter the queryset based on the owner of the course.

    Methods:
        get_queryset(): Filters the queryset to include only objects owned by the current user.
    """

    def get_queryset(self):
        """Return the queryset."""
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)


class OwnerEditMixin:
    """Mixin to set the owner of the course before saving the form.

    Methods:
        form_valid(form): Sets the owner of the form instance to the current user before saving.
    """

    def form_valid(self, form):
        """Set the owner of the form instance to the current user and then validate the form.

        Args:
            form (Form): The form being validated.

        Returns:
            HttpResponse: The HTTP response after form validation.
        """
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    """Mixin for course views that require owner, login, and permission.

    Attributes:
        model (class): The model representing a course.
        fields (list): The fields to include in the course form.
        success_url (str): The URL to redirect to after a successful operation.
    """

    model = Course
    fields = ["subject", "title", "slug", "description"]
    success_url = reverse_lazy("manage_course_list")


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    """Mixin for course edit views that use owner course and owner edit mixins.

    Attributes:
        template_name (str): The template to use for the course form.
    """

    template_name = "courses/manage/course/form.html"


class ManageCourseListView(OwnerCourseMixin, ListView):
    """View to manage the list of courses owned by the user.

    Attributes:
        template_name (str): The template to use for rendering the course list.
        permission_required (str): The permission required to view the course list.
    """

    template_name = "courses/manage/course/list.html"
    permission_required = "courses.view_course"


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    """View to create a new course.

    Attributes:
        permission_required (str): The permission required to add a course.
    """

    permission_required = "courses.add_course"


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    """View to update an existing course.

    Attributes:
        permission_required (str): The permission required to change a course.
    """

    permission_required = "courses.change_course"


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    """View to delete a course.

    Attributes:
        template_name (str): The template to use for confirming the course deletion.
        permission_required (str): The permission required to delete a course.
    """

    template_name = "courses/manage/course/delete.html"
    permission_required = "courses.delete_course"


# ---------------Module View----------------
class CourseModuleUpdateView(TemplateResponseMixin, View):
    """View to update modules for a course.

    Attributes:
        template_name (str): The template to use for the module formset.
        course (Course): The course being updated.

    Methods:
        get_formset(data=None): Returns the formset for the modules.
        dispatch(request, pk): Dispatches the request and sets the course.
        get(request, *args, **kwargs): Renders the module formset.
        post(request, *args, **kwargs): Handles the formset submission.
    """

    template_name = "courses/manage/module/formset.html"
    course = None

    def get_formset(self, data=None):
        """Returns the formset for the modules.

        Args:
            data (dict, optional): The data for the formset.

        Returns:
            FormSet: The formset for the modules.
        """
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        """Dispatches the request and sets the course.

        Args:
            request (HttpRequest): The request object.
            pk (int): The primary key of the course.

        Returns:
            HttpResponse: The response object.
        """
        self.course = get_object_or_404(Course, id=pk, created_by=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """Renders the module formset.

        Args:
            request (HttpRequest): The request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The response object with the module formset.
        """
        formset = self.get_formset()
        return self.render_to_response(
            {"course": self.course, "formset": formset}
        )

    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """Handles the formset submission.

        Args:
            request (HttpRequest): The request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The response object with the module formset.
        """
        formset = self.get_formset(data=request.POST)
        user = request.user

        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.created_by = user
                instance.save()
            formset.save_m2m()
            return redirect("manage_course_list")
        return self.render_to_response(
            {"course": self.course, "formset": formset}
        )


class ModuleContentListView(TemplateResponseMixin, View):
    """View to list the contents of a module.

    Attributes:
        template_name (str): The template to use for the content list.

    Methods:
        get(request, module_id): Renders the content list for a module.
    """

    template_name = "courses/manage/content/content_list.html"

    def get(self, request, module_id):
        """`s the content list for a module.

        Args:
            request (HttpRequest): The request object.
            module_id (int): The ID of the module.

        Returns:
            HttpResponse: The response object with the content list.
        """
        module = get_object_or_404(
            Module, id=module_id, course__created_by=request.user
        )

        module.lessons.set(Lesson.objects.filter(module=module))
        return self.render_to_response({"module": module})


# ----------------Content Views----------------
class ContentCreateUpdateView(TemplateResponseMixin, View):
    """View to create or update content for a module.

    Attributes:
        module (Module): The module to add or update content for.
        model (Model): The model representing the content.
        obj (Model): The instance of the content being updated.
        template_name (str): The template to use for the content form.

    Methods:
        get_model(model_name): Returns the content model based on the model name.
        get_form(model, *args, **kwargs): Returns the form for the content model.
        dispatch(request, module_id, model_name, id=None): Dispatches the request and sets the module and content model.
        get(request, module_id, model_name, id=None): Renders the content form.
        post(request, module_id, model_name, id=None): Handles the content form submission.
    """

    module = None
    model = None
    obj = None

    template_name = "courses/manage/content/form.html"

    def get_model(self, model_name):
        """Returns the content model based on the model name.

        Args:
            model_name (str): The name of the content model.

        Returns:
            Model: The content model.
        """
        if model_name in ["text", "image", "video", "file"]:
            return apps.get_model(app_label="lessons", model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        """Returns the form for the content model.

        Args:
            model (Model): The content model.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Form: The form for the content model.
        """
        form = modelform_factory(
            model, exclude=["created_by", "order", "created", "updated"]
        )
        return form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):  # pylint: disable=redefined-builtin
        """Dispatches the request and sets the module and content model.

        Args:
            request (HttpRequest): The request object.
            module_id (int): The ID of the module.
            model_name (str): The name of the content model.
            id (int, optional): The ID of the content.

        Returns:
            HttpResponse: The response object.
        """
        self.module = get_object_or_404(
            Module, id=module_id, course__created_by=request.user
        )
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(
                self.model, id=id, created_by=request.user
            )
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):  # pylint: disable=unused-argument disable=redefined-builtin
        """Renders the content form.

        Args:
            request (HttpRequest): The request object.
            module_id (int): The ID of the module.
            model_name (str): The name of the content model.
            id (int, optional): The ID of the content.

        Returns:
            HttpResponse: The response object with the content form.
        """
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({"form": form, "object": self.obj})

    def post(self, request, module_id, model_name, id=None):  # pylint: disable=unused-argument disable=redefined-builtin
        """Handles the content form submission.

        Args:
            request (HttpRequest): The request object.
            module_id (int): The ID of the module.
            model_name (str): The name of the content model.
            id (int, optional): The ID of the content.

        Returns:
            HttpResponse: The response object with the content form.
        """
        form = self.get_form(
            self.model,
            instance=self.obj,
            data=request.POST,
            files=request.FILES,
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()

            if not id:
                Lesson.objects.create(
                    module=self.module, item=obj, created_by=request.user
                )
            return redirect("module_content_list", self.module.id)
        return self.render_to_response({"form": form, "object": self.obj})


class ContentDeleteView(View):
    """View to delete content from a module.

    Methods:
        post(request, id): Deletes the content and redirects to the content list.
    """

    def post(self, request, id):  # pylint: disable=redefined-builtin
        """Deletes the content and redirects to the content list.

        Args:
            request (HttpRequest): The request object.
            id (int): The ID of the content to be deleted.

        Returns:
            HttpResponse: The response object redirecting to the content list.
        """
        content = get_object_or_404(
            Lesson, id=id, module__course__created_by=request.user
        )
        module = content.module
        content.item.delete()
        content.delete()
        return redirect("module_content_list", module.id)


# -----------handling the ordering of modules------------
class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """View to handle the ordering of modules.

    Methods:
        post(request): Updates the order of the modules.
    """

    def post(self, request):
        """Updates the order of the modules.

        Args:
            request (HttpRequest): The request object.

        Returns:
            JsonResponse: The JSON response indicating the status.
        """
        for id_key, order in self.request_json.items():
            Module.objects.filter(
                id=id_key, course__created_by=request.user
            ).update(order=order)
        return self.render_json_response({"saved": "ok"})


# -----------handling the ordering of contents------------
class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """View to handle the ordering of contents.

    Methods:
        post(request): Updates the order of the contents.
    """

    def post(self, request):
        """Updates the order of the contents.

        Args:
            request (HttpRequest): The request object.

        Returns:
            JsonResponse: The JSON response indicating the status.
        """
        for id_key, order in self.request_json.items():
            Lesson.objects.filter(
                id=id_key, module__course__created_by=request.user
            ).update(order=order)
        return self.render_json_response({"saved": "ok"})


# Razorpay order Creation

# @login_required
@csrf_exempt
def create_razorpay_order(request):
    if request.method == 'POST':
        try:
            course_id = request.POST.get('course_id')
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            coupon_code = request.POST.get('coupon')

            course = get_object_or_404(Course, id=course_id)

            # Handle coupon code from URL (Fixed `self` reference)
            # coupon_code = request.GET.get("coupon", "").strip()
            final_price = course.price  # Default price

            # Apply coupon discount if available
            if coupon_code:
                coupon = Coupons.objects.filter(coupon_code=coupon_code).first()
                if coupon:
                    final_price = coupon.price  # Use coupon's price

            # Override user details if authenticated
            if request.user.is_authenticated:
                name = request.user.get_full_name() or request.user.username
                email = request.user.email
                phone = getattr(request.user, "phone", phone)  # Keep existing if not available

            # Create Razorpay Order
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            payment = client.order.create({
                "amount": int(float(final_price) * 100),  # Convert to smallest currency unit
                "currency": "INR",
                "payment_capture": 1
            })

            return JsonResponse({
                "key": settings.RAZORPAY_KEY_ID,
                "order_id": payment['id'],
                "course_id": course.id,
                "user_name": name,
                "user_email": email,
                "user_phone": phone,
                "final_price": final_price,  # Include updated price in response
                "callback_url": "https://kalagurubyirarangoliarts.com/accounts/thank_you/",
                "couponCode": coupon_code,
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def my_courses(request):
    user = request.user
    enrollments = Enrollment.objects.filter(user=user, state=True).select_related("course")
    
    return render(request, "courses/my_courses.html", {
        "enrollments": enrollments
    })


# ---------------Course catalog--------------------

class CourseListView(TemplateResponseMixin, View):
    """View to display the list of courses.

    Attributes:
        model (Model): The model representing a course.
        template_name (str): The template to use for rendering the course list.

    Methods:
        get(request, subject=None): Renders the course list based on the subject.
    """
    # login_url = "accounts/login/"  
    # redirect_field_name = "login" 
    model = Course
    template_name = "courses/courses.html"



    def get(self, request, subject=None):  # pylint: disable=unused-argument
        """Renders the course list based on the subject.

        Args:
            request (HttpRequest): The request object.
            subject (str, optional): The slug of the subject to filter courses.

        Returns:
            HttpResponse: The response object with the course list.
        """
        # subjects = cache.get('all_subjects')
        # if not subjects:
        subjects = Subject.objects.annotate(total_courses=Count("courses"))
        # cache.set('all_subjects', subjects)

        # all_courses = Course.objects.annotate(total_modules=Count("modules"))
        all_courses = Course.objects.filter(state=1).annotate(total_modules=Count("modules")).order_by("id")


        today = timezone.now().date()  # Get only the date part

        # Filter courses with enroll_end_date >= today
        all_courses = Course.objects.filter(
            state=1
        ).filter(
            Q(enroll_end_date__gte=today) | Q(enroll_end_date__isnull=True)
        ).order_by("id")[:12]
        # courses = Course.objects.filter(state=1).order_by("id")[:8]  # limit to 8

        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            # key = f'subject_{subject.id}_courses'
            # courses = cache.get(key)
            # if not courses:
            courses = all_courses.filter(subject=subject)
        # cache.set(key, courses)
        else:
            # courses = cache.get('all_courses')
            # if not courses:
            courses = all_courses
            # cache.set('all_courses', courses)
        purchased_course_ids = set()
        if request.user.is_authenticated:
            purchased_course_ids = set(
                Enrollment.objects.filter(user=request.user).values_list("course_id", flat=True)
            )

        return self.render_to_response(
            {
             "subjects": subjects, 
             "subject": subject,
             "courses": courses,
             "purchased_course_ids": purchased_course_ids,
             "today": today,
            }
        )

class CourseDetailView(DetailView):
    """View to display the details of a course with coupon-based pricing."""

    model = Course
    template_name = "courses/detail.html"

    def get(self, request, *args, **kwargs):
        """Handles GET requests and redirects if course state is not True."""
        self.object = self.get_object()

        if not self.object.state:
            messages.error(request, "The course is not available at the moment.")
            return redirect("courses")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Adds additional context data for the template."""
        context = super().get_context_data(**kwargs)

        # Initialize enrollment form
        context["enroll_form"] = CourseEnrollForm(initial={"course": self.object})

        # Prefetch modules & lessons
        modules = self.object.modules.prefetch_related("lessons")
        context["modules"] = modules

        user = self.request.user
        today = timezone.now().date()

        # Determine user enrollment
        enrollment = None
        if user.is_authenticated:
            enrollment = Enrollment.objects.select_related("batch").filter(
                user=user,
                course=self.object,
                state=True
            ).first()

        context["is_enrolled"] = bool(enrollment)

        batch_start_date = None
        if enrollment and enrollment.batch:
            batch_start_date = enrollment.batch.start_date

        context["batch_start_date"] = batch_start_date
        context["today"] = today

        # ---------------------------------------------------
        # Lesson release logic
        # ---------------------------------------------------

        today = timezone.now().date()

        for module in modules:

            lessons = module.lessons.all()
            processed_lessons = []

            for lesson in lessons:

                lesson.can_view = False
                lesson.release_date = None
                lesson.expiry_date = None
                lesson.expired = False
                lesson.locked = False
                lesson.demo = False

                # DEMO lessons
                if lesson.release_after_days == -1:
                    lesson.can_view = True
                    lesson.demo = True

                elif enrollment and batch_start_date:

                    # rule for lesson 0
                    if lesson.release_after_days == 0:
                        release_date = enrollment.enrollment_date.date()

                    else:
                        release_date = batch_start_date + timedelta(days=lesson.release_after_days - 1)

                    expiry_date = release_date + timedelta(days=3)

                    lesson.release_date = release_date
                    lesson.expiry_date = expiry_date

                    if today < release_date:
                        lesson.locked = True

                    elif release_date <= today <= expiry_date:
                        lesson.can_view = True

                    elif today > expiry_date:
                        lesson.expired = True

                processed_lessons.append(lesson)

            module.lessons_with_access = processed_lessons

        # ---------------------------------------------------

        # Handle coupon code
        coupon_code = self.request.GET.get("coupon", "").strip()
        final_price = self.object.price

        if coupon_code:
            coupon = Coupons.objects.filter(coupon_code=coupon_code).first()
            if coupon:
                final_price = coupon.price

        context["final_price"] = final_price
        context["couponCode"] = coupon_code

        return context


# class DashboardView(LoginRequiredMixin, TemplateView):
#     template_name = "accounts/dashboard.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         # Fetch the first course associated with the user
#         user_course = Course.objects.filter(created_by=self.request.user, slug__isnull=False).exclude(slug="").first()

#         # Add course to context
#         context["my_course"] = user_course

#         return context



def mask_phone(phone):
    """Hide middle digits of phone number."""

    if not phone:
        return ""

    phone = str(phone)

    if len(phone) < 6:
        return phone

    return phone[:3] + "*****" + phone[-2:]

def coupon_search(request):
    """
    Public search page to check coupon usage or phone enrollment.
    """

    query = request.GET.get("q", "").strip()

    results = []
    coupon_stats = []

    if query:

        enrollments = Enrollment.objects.filter(
            Q(coupon_code__icontains=query) |
            Q(user__phone__icontains=query)
        ).select_related("user", "course")

        users = {}

        for e in enrollments:

            user = e.user

            if user.id not in users:

                try:
                    student = user.student
                    city = student.district.name if student.district else ""
                except:
                    city = ""

                users[user.id] = {
                    "name": user.get_full_name(),
                    "phone": mask_phone(user.phone),
                    "city": city,
                    "courses": []
                }

            users[user.id]["courses"].append(e.course.title)

        results = users.values()

    # Coupon leaderboard
    coupon_stats = (
        Enrollment.objects.exclude(coupon_code__isnull=True)
        .exclude(coupon_code="")
        .values("coupon_code")
        .annotate(
            total_users=Count("user", distinct=True),
            total_enrollments=Count("id")
        )
        .order_by("-total_enrollments")
    )

    return render(
        request,
        "courses/coupon_search.html",
        {
            "results": results,
            "query": query,
            "coupon_stats": coupon_stats,
        },
    )    