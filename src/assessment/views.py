from django.shortcuts import render ,HttpResponse,redirect
from .models import AssessmentUpload,StudentCompetition
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .forms import StudentCompetitionForm

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

        else:
            return HttpResponse("Invalid file type. Please upload PNG or JPG.", status=400)

    return render(request, 'upload.html')


def thankyou(request):
    return render (request,'thankyou.html')



# Check if user is superuser
def is_superuser(user):
    return user.is_superuser

# @user_passes_test(is_superuser)
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
def student_competition_edit(request, pk):
    competition = StudentCompetition.objects.get(pk=pk)
    if request.method == 'POST':
        form = StudentCompetitionForm(request.POST, instance=competition)
        if form.is_valid():
            form.save()
            return redirect('student_competition_list')
    else:
        form = StudentCompetitionForm(instance=competition)
    return render(request, 'student_competition_form.html', {'form': form})

@user_passes_test(is_superuser)
def student_competition_delete(request, pk):
    competition = StudentCompetition.objects.get(pk=pk)
    competition.delete()
    return redirect('student_competition_list')
