from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
from .models import AssessmentUpload, StudentCompetition
from .forms import ReviewForm, StudentCompetitionForm

# Upload Work
@login_required
def upload(request):
    if not StudentCompetition.objects.filter(user=request.user, status=1).exists():
        return HttpResponse("You are not allowed to upload files.", status=403)

    if request.method == 'POST' and request.FILES.get('work'):
        file = request.FILES['work']
        current_date = datetime.now().strftime('%Y%m%d')
        formatted_filename = f'{file.name.split(".")[0]}_{request.user.id}_{current_date}.{file.name.split(".")[-1]}'

        if file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_data = file.read()

            assessment = AssessmentUpload.objects.create(
                user_id=request.user,
                work=file_data,
                filename=formatted_filename,
                content_type=file.content_type
            )

            return render(request, 'thankyou.html')

        return HttpResponse("Invalid file type. Please upload PNG or JPG.", status=400)

    return render(request, 'upload.html')

def thankyou(request):
    return render(request, 'thankyou.html')

# Admin Functions
def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def student_competition_list(request):
    competitions = StudentCompetition.objects.all()
    return render(request, 'assessment/student_competition_list.html', {'competitions': competitions})

@user_passes_test(is_superuser)
def student_competition_add(request):
    if request.method == 'POST':
        form = StudentCompetitionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_competition_list')
    else:
        form = StudentCompetitionForm()
    return render(request, 'assessment/student_competition_form.html', {'form': form})

@user_passes_test(is_superuser)
def student_competition_edit(request, competition_id):
    competition = get_object_or_404(StudentCompetition, id=competition_id)
    if request.method == 'POST':
        form = StudentCompetitionForm(request.POST, instance=competition)
        if form.is_valid():
            form.save()
            return redirect('student_competition_list')
    else:
        form = StudentCompetitionForm(instance=competition)
    return render(request, 'assessment/student_competition_form.html', {'form': form})

@user_passes_test(is_superuser)
def student_competition_delete(request, competition_id):
    competition = get_object_or_404(StudentCompetition, id=competition_id)
    competition.delete()
    return redirect('student_competition_list')

# Teacher Functions
@login_required
def assigned_work_list(request):
    if not request.user.groups.filter(name='Teachers').exists():
        return HttpResponse("Unauthorized", status=403)

    assigned_works = AssessmentUpload.objects.filter(assigned_teacher=request.user)
    return render(request, 'assessment/assigned_work_list.html', {'assigned_works': assigned_works})

@login_required
def submit_review(request, work_id):
    if not request.user.groups.filter(name='Teachers').exists():
        return HttpResponse("Unauthorized", status=403)

    work = get_object_or_404(AssessmentUpload, id=work_id, assigned_teacher=request.user)

    if request.method == 'POST':
        score = int(request.POST.get('review_score', 0))
        if score < 1 or score > 5:
            return HttpResponse("Invalid score", status=400)

        work.review_score = score
        work.save()
        return redirect('assigned_work_list')

    return render(request, 'assessment/review_form.html', {'work': work})

# Edit & Delete Work Submission
@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='Teachers').exists())  
def edit_work(request, work_id):
    work = get_object_or_404(AssessmentUpload, id=work_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=work)
        if form.is_valid():
            form.save()
            return redirect('assigned_work_list')
    else:
        form = ReviewForm(instance=work)
    return render(request, 'assessment/review_form.html', {'form': form, 'work': work})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_work(request, work_id):
    work = get_object_or_404(AssessmentUpload, id=work_id)
    work.delete()
    return redirect('assigned_work_list')
