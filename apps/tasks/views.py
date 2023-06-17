from django.shortcuts import render, redirect, get_object_or_404
from apps.tasks.models import Tasks, Themes, Comments, Points, Files
from apps.cources.models import Cources, CourceStream
from apps.tasks.forms import TaskForms, PointForm, FileForm, ChangeTaskForms
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse


def cource_tasks(request, pk):
    cource = Cources.objects.get(pk=pk)
    tasks = Tasks.objects.filter(cource=cource).order_by('-added_at')
    themes = Themes.objects.filter(cource=cource)
    nav2 = 'active'
    return render(request, 'cource/tasks.html', locals())

def add_task(request, pk):
    cource = Cources.objects.get(pk=pk)
    themes = Themes.objects.filter(cource=cource)
    user = request.user
    form = TaskForms()
    if request.method == 'POST':
        form = TaskForms(request.POST, request.FILES)
        if form.is_valid():
            name = request.POST['name']
            instruction = request.POST['instruction']
            file = form.cleaned_data['file']
            points = form.cleaned_data['points']
            deadline = form.cleaned_data['deadline']
            theme = request.POST.get('theme')
            new_theme = request.POST['new_theme']
        if name and instruction:
            if theme:
                theme = Themes.objects.get(name=theme)
                task = Tasks(
                    name = name,
                    instruction = instruction,
                    file = file,
                    points = points,
                    deadline = deadline,
                    theme = theme,
                    cource = cource,
                    added_by = user
                )
                task.save()
                stream = CourceStream(
                    text = f'Пользователь {request.user.username} добавил задание: {task.name}',
                    cource = cource,
                    user = request.user
                )
                stream.save()
                return redirect('cource-tasks', pk=pk)
            elif new_theme:
                try:
                    newtheme = Themes(
                        name = new_theme,
                        cource = cource
                    )
                    newtheme.save()
                    task = Tasks(
                        name = name,
                        instruction = instruction,
                        file = file,
                        points = points,
                        deadline = deadline,
                        theme = newtheme,
                        cource = cource,
                        added_by = user
                    )
                    task.save()
                    stream = CourceStream(
                        text = f'Пользователь {request.user.username} добавил задание: {task.name}',
                        cource = cource,
                        user = request.user
                    )
                    stream.save()
                    return redirect('cource-tasks', pk=pk)
                except Exception:
                    theme = Themes.objects.get(name=new_theme)
                    task = Tasks(
                        name = name,
                        instruction = instruction,
                        file = file,
                        points = points,
                        deadline = deadline,
                        theme = theme,
                        cource = cource,
                        added_by = user
                    )
                    task.save()
                    stream = CourceStream(
                        text = f'Пользователь {request.user.username} добавил задание: {task.name}',
                        cource = cource,
                        user = request.user
                    )
                    stream.save()
                    return redirect('cource-tasks', pk=pk)
            else:
                task = Tasks(
                    name = name,
                    instruction = instruction,
                    file = file,
                    points = points,
                    deadline = deadline,
                    cource = cource,
                    added_by = user
                )
                task.save()
                stream = CourceStream(
                    text = f'Пользователь {request.user.username} добавил задание: {task.name}',
                    cource = cource,
                    user = user
                )
                stream.save()
                return redirect('cource-tasks', pk=pk)
    return render(request, 'cource/addtask.html', locals())
    

def task_detail(request, pk):
    task = Tasks.objects.get(pk=pk)
    comments = Comments.objects.filter(task=task)
    user = request.user
    if Files.objects.filter(Q(task=task) & Q(student=user)).exists():
        file = Files.objects.get(Q(task=task) & Q(student=user))
    if Points.objects.filter(Q(student=user) & Q(task=task)).exists():
        point = Points.objects.get(Q(student=user) & Q(task=task))
    if request.method == 'POST':
        comment = Comments(
            text = request.POST['comment'],
            user = request.user,
            task = task
        )
        comment.save()
        return redirect('task-detail', pk=pk)
    return render(request, 'cource/task-detail.html', locals())


def all_points(request, pk):
    cource = Cources.objects.get(pk=pk)
    tasks = Tasks.objects.filter(cource=cource)
    files = Files.objects.all()
    nav4 = 'active'
    return render(request, 'cource/point.html', locals())


def task_points(request, pk):
    task = Tasks.objects.get(pk=pk)
    cource = task.cource
    students = cource.students.all()
    points = Points.objects.filter(task=task)
    files = Files.objects.filter(task=task)
    works = files.count()
    all_students = students.count()
    if points:
        return render(request, 'cource/added-points.html', locals())
    if request.method == 'POST':
        for student in students:
            username = student.username
            given_point = request.POST[username]
            point = Points(
                points = given_point, 
                student = student,
                task = task
            )
            point.save()
        task = Tasks.objects.get(pk=pk)
        cource = task.cource
        students = cource.students.all()
        points = Points.objects.filter(task=task)
        files = Files.objects.filter(task=task)
        works = files.count()
        all_students = students.count()
        return render(request, 'cource/added-points.html', locals())
    return render(request, 'cource/add-points.html', locals())


def update_points(request, pk):
    point = get_object_or_404(Points, pk=pk)
    task = point.task
    if request.method == 'POST':
        form = PointForm(request.POST, instance=point)
        if form.is_valid():
            form.save()
        return redirect('task-points', pk=task.pk)
    else:
        form = PointForm(instance=point)
    return render(request, 'cource/update-point.html', locals())


def add_file(request, pk):
    task = Tasks.objects.get(pk=pk)
    if request.method == 'POST':
        file = request.FILES.get('file')
        f = Files(
            file = file,
            student = request.user,
            task = task
        )
        f.save()
        messages.info(request, 'Файл добавлен')
        return redirect('task-detail', pk=pk)
    return render(request, 'cource/add-file.html', locals())


def change_file(request, pk):
    file = get_object_or_404(Files, pk=pk)
    if request.method == 'POST':
       form =  FileForm(request.POST, request.FILES, instance=file)
       if form.is_valid():
           form.save()
           return redirect('task-detail', pk=file.task.pk)
    else:
        form = FileForm(instance=file)
    return render(request, 'cource/change-file.html', locals())


def change_task(request, pk):
    task = get_object_or_404(Tasks, pk=pk)
    if request.method == 'POST':
        form = ChangeTaskForms(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task-detail', pk=pk)
    form = ChangeTaskForms(instance=task)
    return render(request, 'cource/change-task.html', locals())

