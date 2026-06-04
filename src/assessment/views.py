import os
from datetime import datetime
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from assessment.forms import ReviewForm, StudentCompetitionForm
from assessment.models import AssessmentUpload, StudentCompetition



@login_required
def login_redirect(request):
    """Redirect users to the correct dashboard based on their role."""
    if hasattr(request.user, "is_lecturer") and request.user.is_lecturer:
        return redirect("assigned_work_list")
    if not StudentCompetition.objects.filter(
        user=request.user, status=1
    ).exists():
        return HttpResponse("You are student not register for competition...!")
    if request.user.is_superuser:
        return redirect("student_competition_list")
    return redirect("upload")


# Upload Work
@login_required
def upload(request):
    has_submitted = AssessmentUpload.objects.filter(user_id=request.user).exists()
    if has_submitted:
        return render(request, "assessment/upload.html", {
            "has_submitted": has_submitted
        })

    if request.method == "POST" and request.FILES.get("work"):
        file = request.FILES["work"]

        if file.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
            return HttpResponse(
                "File too large. Maximum allowed size is 5 MB. Please upload file less than 5 MB.",
                status=400
            )

        if not file.name.lower().endswith((".png", ".jpg", ".jpeg")):
            return HttpResponse(
                "Invalid file type. Please upload PNG or JPG.",
                status=400
            )

        # Generate file path and filename
        current_date = datetime.now().strftime("%Y%m%d")
        ext = file.name.split(".")[-1]
        filename = f"{file.name.split('.')[0]}_{request.user.id}_{current_date}.{ext}"
        relative_path = f"assignment/{filename}"
        save_path = os.path.join(settings.BASE_DIR, 'static', relative_path)

        # Ensure folder exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Save file to disk
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Save file path (relative) in DB
        AssessmentUpload.objects.create(
            user_id=request.user,
            work=relative_path,  # relative path saved to DB
            filename=filename,
            content_type=file.content_type,
        )

        return render(request, "assessment/thankyou.html")

    return render(request, "assessment/upload.html")


def thankyou(request):
    """Render the thank-you page after a successful submission."""
    return render(request, "assessment/thankyou.html")


# Admin Functions
def is_superuser(user):
    """Check if the given user is a superuser.

    Returns:
        bool: True if the user is a superuser, False otherwise.
    """
    return user.is_superuser


@user_passes_test(is_superuser)
def student_competition_list(request):
    """Display a list of all student competitions.

    This view is accessible only to superusers.
    Retrieves all student competitions and renders them in a template.
    """
    competitions = StudentCompetition.objects.all()
    return render(
        request,
        "assessment/student_competition_list.html",
        {"competitions": competitions},
    )


@user_passes_test(is_superuser)
def student_competition_add(request):
    """Handle the creation of a new student competition.

    This view is accessible only to superusers.
    It processes form submissions for adding a new student competition.
    """
    if request.method == "POST":
        form = StudentCompetitionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student_competition_list")
    else:
        form = StudentCompetitionForm()
    return render(
        request, "assessment/student_competition_form.html", {"form": form}
    )


@user_passes_test(is_superuser)
def student_competition_edit(request, competition_id):
    """Edit an existing student competition.

    Retrieves a competition by ID and allows superusers
    to update its details using a form submission.
    """
    competition = get_object_or_404(StudentCompetition, id=competition_id)
    if request.method == "POST":
        form = StudentCompetitionForm(request.POST, instance=competition)
        if form.is_valid():
            form.save()
            return redirect("student_competition_list")
    else:
        form = StudentCompetitionForm(instance=competition)
    return render(
        request, "assessment/student_competition_form.html", {"form": form}
    )


@user_passes_test(is_superuser)
def student_competition_delete(competition_id):
    """Delete an existing student competition.

    This function removes the specified competition based on its ID.
    """
    competition = get_object_or_404(StudentCompetition, id=competition_id)
    competition.delete()
    return redirect("student_competition_list")


# Lecturer (Teacher) Functions
@login_required
def assigned_work_list(request):
    """Display a list of assigned student works.

    This view retrieves and shows all works assigned to teachers for review.
    """
    if not request.user.is_lecturer:
        return HttpResponse("Unauthorized", status=403)

    assigned_works = AssessmentUpload.objects.filter(
        assigned_teacher=request.user
    )
    return render(
        request,
        "assessment/assigned_work_list.html",
        {"assigned_works": assigned_works},
    )


@login_required
def submit_review(request, work_id):
    """Submit a review for a student's work.

    This view allows a teacher to provide a rating and comments
    for an assigned student submission.
    """
    if not request.user.is_lecturer:
        return HttpResponse("Unauthorized", status=403)

    work = get_object_or_404(
        AssessmentUpload, id=work_id, assigned_teacher=request.user
    )

    if request.method == "POST":
        score = int(request.POST.get("review_score", 0))
        if score < 1 or score > 5:
            return HttpResponse("Invalid score", status=400)

        work.review_score = score
        work.save()
        return redirect("assigned_work_list")

    return render(request, "assessment/review_form.html", {"work": work})


# Edit & Delete Work Submission
@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_lecturer)
def edit_work(request, work_id):
    """Edit a submitted student work.

    This view allows authorized users to update the details of
    a specific student work based on its ID.
    """
    work = get_object_or_404(AssessmentUpload, id=work_id)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=work)
        if form.is_valid():
            form.save()
            return redirect("assigned_work_list")
    else:
        form = ReviewForm(instance=work)
    return render(
        request, "assessment/review_form.html", {"form": form, "work": work}
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_work(work_id):
    """Delete a submitted student work.

    This function removes a specific student work from the database based on its ID.
    """
    work = get_object_or_404(AssessmentUpload, id=work_id)
    work.delete()
    return redirect("assigned_work_list")
