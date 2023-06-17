from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from apps.cources.models import Cources, CourceStream, StreamComments, PrivateRoom, Messages
from apps.tasks.models import Tasks
from django.db.models import Q
from django.contrib import messages
from django.contrib import auth 
from datetime import datetime
import calendar


User = get_user_model()

def all_cources(request):
    if request.user.is_authenticated:
        user = request.user
        student = Cources.objects.filter(students=user)
        teacher = Cources.objects.filter(teachers=user)
        cources = student.union(teacher)
        nav1 = 'active'
        return render(request, 'homepage/index.html', locals())
    else:
        return redirect('register')


def is_teacher(request):
    user = request.user
    cources = Cources.objects.filter(teachers=user)
    nav2 = 'active'
    return render(request, 'homepage/index.html', locals())


def is_student(request):
    user = request.user
    cources = Cources.objects.filter(students=user)
    nav3 = 'active'
    return render(request, 'homepage/index.html', locals())


def add_cource(request):
    nav4 = 'active'
    if request.method == 'POST':
        name = request.POST['name']
        subject = request.POST['subject']
        user = request.user
        cource = Cources(
            name = name,
            subject = subject,
            owner = user
        )
        cource.save()
        cource.teachers.add(user)
        return redirect('teacher')
    return render(request, 'homepage/addcource.html', locals())


def join_cource(request):
    nav5 = 'active'
    if request.method == 'POST':
        code = request.POST['code']
        try:
            cource = Cources.objects.get(code=code)
            user = request.user
            if user in cource.students.all():
                messages.info(request, 'Вы уже состоите в группе!')
                return redirect('join-cource')
            cource.students.add(request.user)
            messages.info(request, f'Вы присоединились группе {cource.name}')
            return redirect('join-cource')
        except Exception:
            messages.info(request, 'Курс не найден!')
            return redirect('join-cource')
    return render(request, 'homepage/join-cource.html', locals())


def cource_stream(request, pk):
    cource = Cources.objects.get(pk=pk)
    streams = CourceStream.objects.filter(cource=cource)
    stream_comments = StreamComments.objects.all()
    nav1 = 'active'
    if request.method == 'POST':
        text = request.POST['text']
        if text:
            stream = CourceStream(
                text = text,
                is_group_message = True,
                cource = cource,
                user = request.user
            )
            stream.save()
            return redirect('cource-stream', pk=pk)
    return render(request, 'cource/stream.html', locals())


def add_stream_comment(request):
    if request.method == 'POST':
        stream_pk = request.POST['hidden']
        stream = CourceStream.objects.get(pk=stream_pk)
        stream_comment = StreamComments(
            text = request.POST['text'], 
            stream = stream,
            user = request.user
        )
        stream_comment.save()
        return redirect(request.META['HTTP_REFERER'])
    

def users(request, pk):
    cource = Cources.objects.get(pk=pk)
    teachers = cource.teachers.all().order_by('id')
    students = cource.students.all()
    if request.method == 'POST':
        name = request.POST.get('button')
        user = User.objects.get(username=name)
        if user in cource.students.all():
            cource.students.remove(user)
            return redirect(request.META.get('HTTP_REFERER', '/'))
        elif user in cource.teachers.all():
            cource.teachers.remove(user)
            return redirect(request.META.get('HTTP_REFERER', '/'))
    nav3 = 'active'
    return render(request, 'cource/users.html', locals())


def add_teacher(request, pk):
    cource = Cources.objects.get(pk=pk)
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user in cource.teachers.all() or user in cource.students.all():
                messages.info(request, 'Пользователь уже состоит в группе!')
                return redirect('add-teacher', pk=pk)
            cource.teachers.add(user)
            return redirect('users', pk=pk)
        messages.info(request, 'Пользователь не найден!')
        return redirect('add-teacher', pk=pk)
    return render(request, 'cource/add-teacher.html', locals())


def add_student(request, pk):
    cource = Cources.objects.get(pk=pk)
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user in cource.teachers.all() or user in cource.students.all():
                messages.info(request, 'Пользователь уже состоит в группе!')
                return redirect('add-student', pk=pk)
            cource.students.add(user)
            return redirect('users', pk=pk)
        messages.info(request, 'Пользователь не найден!')
        return redirect('add-student', pk=pk)
    return render(request, 'cource/add-student.html', locals())

def login_view(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password1']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('allcources')  # Replace 'home' with the URL name of your home page
        else:
            # Handle invalid login credentials
            messages.info(request, 'Invalid data!')
            return render(request, 'homepage/login.html')
    else:
        return render(request, 'homepage/login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
            username = request.POST['name']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1==password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username taken')
                    return redirect('register')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'email taken')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.save()
                    login(request, user)
                    return redirect('allcources')
            else:
                messages.info(request, 'password is not matching...')
                return redirect('register')
    return render(request, 'homepage/register.html', locals())


def delete_cource(request, pk):
    cource = Cources.objects.get(pk=pk)
    cource.delete()
    return redirect('allcources')

def leave_cource(request, pk):
    cource = Cources.objects.get(pk=pk)
    user = request.user
    if user in cource.teachers.all():
        cource.teachers.remove(user)
        return redirect('allcources')
    elif user in cource.students.all():
        cource.students.remove(user)
        return redirect('allcources')
    

def private_room(request, pk):
    user1 = User.objects.get(pk=pk)
    try:
        room = PrivateRoom.objects.get(Q(student=user1) & Q(teacher=request.user))
    except Exception:
        room = PrivateRoom(
            student = user1,
            teacher = request.user,
        )
        room.save()
    messages = Messages.objects.filter(room=room)
    if request.method == 'POST':
        text = request.POST['text']
        m = Messages(
            message = text,
            sent_by = request.user,
            room = room
        )
        m.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'cource/private.html', locals())
    

def teacher_private(request, pk):
    user1 = User.objects.get(pk=pk)
    try:
        room = PrivateRoom.objects.get(Q(student=request.user) & Q(teacher=user1))
    except Exception:
        room = PrivateRoom(
            teacher = user1,
            student = request.user,
        )
        room.save()
    messages = Messages.objects.filter(room=room)
    if request.method == 'POST':
        text = request.POST['text']
        m = Messages(
            message = text,
            sent_by = request.user,
            room = room
        )
        m.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'cource/private.html', locals())


def comming_tasks(request, pk):
    cource = Cources.objects.get(pk=pk)
    current_date = datetime.now().date()
    start_time = str(current_date)
    end_day = current_date.day + 7
    cal = calendar.month(current_date.year, current_date.month)
    day = cal.split(' ')[-1]
    current_day = day[:2]
    year = current_date.year
    month = current_date.month
    if end_day > int(current_day):
        month = current_date.month + 1
        if month > 12:
            year = current_date.year + 1
            month = 1
        end_day = end_day - int(current_day)
    end_time = str(str(year), str(month), str(end_day))
    nav5 = 'active'

    tasks = Tasks.objects.filter(deadline__gte=start_time, deadline__lte = end_time)
    return render(request, 'cource/comming-tasks.html', locals())
