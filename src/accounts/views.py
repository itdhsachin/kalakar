"""Views for the accounts app.

This module contains view functions for rendering profiles in the accounts application.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.forms import StudentForm, TeacherForm
from accounts.models import Session, Student, Teacher, User


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
        context['user_profile'] = teacher

        return render(request, "accounts/profile.html", context)

    if request.user.is_student:
        # print("student")
        # get_object_or_404(Student, student__pk=request.user.id)
        # courses = TakenCourse.objects.filter(
        #     student__student__id=request.user.id, course__level=student.level
        # )
        try:
            student = Student.objects.get(student=request.user)
            # print (student)
            # print (" value :" , student.student.first_name)
            student.refresh_from_db()
            context['user_profile'] = student  # Add student to context if needed
        except Student.DoesNotExist:
            context['error'] = "Student profile not found."
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
    if request.user.is_authenticated:
         
        user = request.user
        is_teacher = hasattr(user, 'teacher')
        is_student = hasattr(user, 'student')
        # Check if the logged-in user is a student or teacher and initialize the corresponding form
        if hasattr(request.user, 'student'):
            student = request.user.student
            form = StudentForm(request.POST or None, instance=student, user=request.user)  # Pass user instance
        elif hasattr(request.user, 'teacher'):
            teacher = request.user.teacher
            form = TeacherForm(request.POST or None, instance=teacher, user=request.user)  # Pass user instance
        else:
            form = None  # For other users or admins (if applicable)

        if request.method == 'POST' and form:
            if form.is_valid():
                form.save()  
                user = request.user  
                user.first_name = form.cleaned_data.get('first_name', user.first_name)
                user.last_name = form.cleaned_data.get('last_name', user.last_name)
                user.email = form.cleaned_data.get('email', user.email)
                user.phone = form.cleaned_data.get('phone', user.phone)
                user.save()
                return redirect('profile')  
            else:
                print(form.errors)  

        # Render the update profile form
        return render(request, 'accounts/update_profile.html', {'form': form ,'is_teacher': is_teacher, 'is_student': is_student})
    else:
        return redirect('login')