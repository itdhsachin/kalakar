"""Views for the accounts app.

This module contains view functions for rendering profiles in the accounts application.
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.forms import SetPasswordForm 
from django.shortcuts import redirect, render,get_object_or_404
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.http import JsonResponse,HttpResponseForbidden
from accounts.forms import CustomPasswordResetForm, StudentForm, TeacherForm
from accounts.models import Session, Student, Teacher, User,District,State
from django.contrib.auth import logout
from courses.models import Course,Enrollment,Certificate
from assessment.models import StudentCompetition,CompetitionDetails,AssessmentUpload
from lessons.models import LessonTrack
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template



@login_required
def profile(request):
    """Show profile of the current user.

    This view function renders the profile.html template with the context specific to the
    current user, including user-specific data and courses.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response with the rendered template.
    """
    current_session = Session.objects.filter(is_current_session=True).first()

    context = {
        "title": request.user.get_full_name,
        "current_session": current_session,
    }

    if request.user.is_lecturer:
        # @TODO add user courses in context
        # courses = Course.objects.filter(
        #     allocated_course__lecturer__pk=request.user.id, semester=current_semester
        # )
        # context["courses"] = courses
        # print("teacher")
        teacher = Teacher.objects.get(teacher=request.user)
        teacher.refresh_from_db()
        context["user_profile"] = teacher

        return render(request, "accounts/profile.html", context)

    if request.user.is_student:
        # print("student")
        # get_object_or_404(Student, student__pk=request.user.id)
        # courses = TakenCourse.objects.filter(
        #     student__student__id=request.user.id, course__level=student.level
        # )
        try:
            student = Student.objects.get(student=request.user)
            student.refresh_from_db()
            context["user_profile"] = (
                student  # Add student to context if needed
            )
        except Student.DoesNotExist:
            context["error"] = "Student profile not found."
            return render(request, "accounts/profile.html", context)
        # @TODO add user courses in context
        # context.update(
        #     {
        #         # "courses": courses,
        #         # "level": student.level,
        #         "dummy": "dummy"
        #     }
        # )
        return render(request, "accounts/profile.html", context)

    # For superuser or other staff
    staff = User.objects.filter(is_lecturer=True)
    context["staff"] = staff
    return render(request, "accounts/profile.html", context)


# update profile function
@login_required
def update_profile(request):
    """Update the profile of the logged-in user based on their role (student or teacher)."""
    user = request.user
    is_teacher = hasattr(user, "teacher")
    is_student = hasattr(user, "student")

    form = None
    user_profile = None

    if is_student:
        student = user.student
        form = StudentForm(
            request.POST or None,
            request.FILES or None,
            instance=student,
            user=user,
        )
        user_profile = student

    elif is_teacher:
        teacher = user.teacher
        form = TeacherForm(
            request.POST or None,
            request.FILES or None,
            instance=teacher,
            user=user,
        )
        user_profile = teacher

    if request.method == "POST" and form:
        if form.is_valid():
            form.save()
            # Update base User model fields
# Only update first_name if it's empty
            if not user.first_name:
                first_name = form.cleaned_data.get("first_name")
                if first_name:
                    user.first_name = first_name

            # Only update last_name if it's empty
            if not user.last_name:
                last_name = form.cleaned_data.get("last_name")
                if last_name:
                    user.last_name = last_name

            user.email = form.cleaned_data.get("email", user.email)
            user.phone = form.cleaned_data.get("phone", user.phone)
            user.save()

            # Handle "Other" state
            other_state = form.cleaned_data.get("other_state")
            if other_state:
                state, created = State.objects.get_or_create(name=other_state)
                if is_student:
                    student.state = state

            # Handle "Other" district
            other_district = form.cleaned_data.get("other_district")
            if other_district:
                state = student.state if is_student else teacher.state
                if state:
                    district, created = District.objects.get_or_create(name=other_district, state=state)
                    if is_student:
                        student.district = district

            if is_student:
                student.save()

            return redirect("profile")
        else:
            messages.error(request, "There was an error updating your profile. Please check the form.")

    return render(
        request,
        "accounts/update_profile.html",
        {
            "form": form,
            "is_teacher": is_teacher,
            "is_student": is_student,
            "user_profile": user_profile,
        },
    )


class CustomPasswordResetView(PasswordResetView):
    """Custom password reset view to override default templates."""

    template_name = "accounts/password_reset.html"
    html_email_template_name  = "accounts/password_reset_email.html"
    subject_template_name = "accounts/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")
    form_class = CustomPasswordResetForm

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Custom view for confirming the password reset and setting a new password."""
    template_name = "accounts/password_reset_confirm.html"
    form_class = SetPasswordForm  # You can replace this with your custom form if needed
    success_url = reverse_lazy("password_reset_complete")
@login_required
def dashboard(request):
    """Render the user dashboard."""
    user = request.user
    course = Course.objects.first()
    # competition = StudentCompetition.objects.filter(user=request.user).exists()
    competition = CompetitionDetails.objects.first()
    total_lessons = competition.total_lessons_required if competition else 1
    course_end_date = competition.course_end_date if competition else timezone.now().date()
    attended_lessons = LessonTrack.objects.filter(user=user).count()
    attendance_percentage = (attended_lessons / total_lessons) * 100 if total_lessons > 0 else 0
    enrollments = Enrollment.objects.filter(user=user, state=True).select_related('course')
    certificates_data = []
    today = timezone.now().date()
    
    for enrollment in enrollments:
        course = enrollment.course
        start_date = course.enroll_start_date
        end_date = course.end_date
        is_available = False
        if start_date and end_date:
            is_available = start_date <= today <= end_date
        
        # Check if a certificate template exists (optional)
        template_name = f"accounts/certificate/certificate_{course.id}.html"
        
        # Check certificate period: between course start and end date
        certificate = Certificate.objects.filter(user=user, course=course, state=True).first()
        
        # If certificate exists and is in the valid period
        certificates_data.append({
            'course_id': course.id,
            'course_name': course.title,
            'certificate_url': reverse('certificate_detail', args=[course.id]),
            'is_available' : is_available

        })

    single_certificate = len(certificates_data) == 1
    multiple_certificates = len(certificates_data) > 1

    # is_eligible = timezone.now().date() >= course_end_date
    # certificate and submit work percentage
    show_button = attendance_percentage > 50 and timezone.now().date() >= course_end_date

    # if is_eligible:
    #     student_competition, created = StudentCompetition.objects.get_or_create(
    #     user=user, defaults={"status": 1}
    #     )
    if user.is_student:
        try:
            student = Student.objects.get(student=user)

            # List of fields to check
            profile_fields = [
                student.full_name, student.gender, student.birthday, student.education,
                student.address, student.taluka, student.district, student.state,
                student.pincode, student.ira_rangoli_reference, student.hobbies
            ]

            # Mandatory fields (always filled)
            mandatory_fields = [user.first_name, user.last_name, user.email, user.phone]

            # Count filled fields
            filled_fields_count = sum(bool(field) for field in profile_fields + mandatory_fields)
            total_fields = len(profile_fields) + len(mandatory_fields)

            # Calculate percentage
            profile_completion = (filled_fields_count / total_fields) * 100
            profile_completion = round(profile_completion / 5) * 5
            # has_submitted = AssessmentUpload.objects.filter(user_id=user).exists()
        except Student.DoesNotExist:
            profile_completion = 0  

    else:
        profile_completion = 100 
    return render(request, "accounts/dashboard.html", {
        "course": course, 
        "profile_completion": round(profile_completion, 2), 
        "show_message": profile_completion < 85,
        "certificates_data": certificates_data,
        "single_certificate": single_certificate,
        "multiple_certificates": multiple_certificates,
        # "has_submitted" : has_submitted
    })

@csrf_exempt
def thank_you(request):
    """Render the user dashboard."""
    return render(request, "accounts/thank_you.html")



@login_required
def logout_view(request):
    logout(request)
    return render(request , "logged_out.html")

@login_required
def certificate_view(request):
    """Generate a certificate with course name, user's name, and today's date."""
    user = request.user
    course = Course.objects.first() 

    context = {
        "user_name": f"{user.first_name} {user.last_name}",
        "course_name": course.title,
        "date_today": timezone.now().strftime("%d-%m-%Y"), 
    }

    return render(request, "accounts/certificate.html", context)


def get_districts(request):
    state_id = request.GET.get("state_id")  # This gets state_id from AJAX
    if state_id:
        districts = District.objects.filter(state_id=state_id).values("id", "name")
        return JsonResponse(list(districts), safe=False)
    return JsonResponse([], safe=False)


@login_required
def certificate_detail(request, course_id):
    """Render the certificate for a specific course."""
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    enrollment = Enrollment.objects.filter(user=user, course=course, state=True).first()
    
    if not enrollment:
        return HttpResponseForbidden("You are not enrolled in this course.")
    
    today = timezone.now().date()
    certificate = Certificate.objects.filter(user=user, course=course, state=True).first()
    
    # if not certificate or not (certificate.issue_date <= today and (not certificate.eol_date or today <= certificate.eol_date)):
    #     return HttpResponseForbidden("Certificate is not available for this course at this time.")
    
    # Create an entry if not already created
    if not certificate.certificate_url:
        # Here you can set the certificate_url if you need to track downloads
        certificate.certificate_url = f"/certificates/{course.id}/{user.id}"
        certificate.save()
    
    template_name = f"accounts/certificate/certificate_{course.id}.html"
    

    try:
        get_template(template_name)
    except :
        print("template not exist")
    

    
    context = {
        "user_name": f"{user.first_name} {user.last_name}",
        "course_name": course.title,
        "date_today": timezone.now().strftime("%d-%m-%Y"),
        "certificate": certificate,
    }
    
    return render(request, template_name, context)

@login_required
def certificate_download(request, course_id):
    """Track certificate download and create Certificate entry if needed."""
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    enrollment = Enrollment.objects.filter(user=user, course=course, state=True).first()
    if not enrollment:
        return HttpResponseForbidden("You are not enrolled in this course.")

    today = timezone.now().date()
    certificate = Certificate.objects.filter(user=user, course=course, state=True).first()

    # If the certificate does not exist yet, create it NOW:
    if not certificate:
        certificate = Certificate.objects.create(
            user=user,
            course=course,
            issue_date=today,
            state=True,
            certificate_url=f"/certificates/{course.id}/{user.id}",
            created_by=request.user
        )
    elif not certificate.certificate_url:
        # Add URL if missing
        certificate.certificate_url = f"/certificates/{course.id}/{user.id}"
        certificate.save()

    # You can also track download timestamp here if needed:
    # certificate.last_downloaded = timezone.now()
    # certificate.save()

    # Load certificate template:
    template_name = f"accounts/certificate/certificate_{course.id}.html"
    try:
        get_template(template_name)
    except:
        template_name = "accounts/certificate/default_certificate.html"

    context = {
        "user_name": f"{user.first_name} {user.last_name}",
        "course_name": course.title,
        "date_today": timezone.now().strftime("%d-%m-%Y"),
        "certificate": certificate,
    }
    return render(request, template_name, context)



@login_required
def certificate_list(request):
    """Show the list of all available certificates for the user (even if not downloaded yet)."""
    user = request.user
    enrollments = Enrollment.objects.filter(user=user, state=True).select_related('course')
    certificates_data = []
    today = timezone.now().date()

    for enrollment in enrollments:
        course = enrollment.course
        start_date = course.enroll_start_date
        end_date = course.end_date
        is_available = False
        if start_date and end_date:
            is_available = start_date <= today <= end_date
        # We don’t care if certificate exists or not, we just show the course.
        certificates_data.append({
            'course_id': course.id,
            'course_name': course.title,
            'download_url': reverse('certificate_download', args=[course.id]),
            'is_available' : is_available,
        })

    return render(request, "accounts/certificate_list.html", {
        "certificates_data": certificates_data,
    })
