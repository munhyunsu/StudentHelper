from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext

from advice.models import Question

def index(request):
    return render(request, 'index.html')


def smain(request):
    if request.method == 'GET':
        method = request.method
        user = request.user
        all_posts = Question.objects.all().filter(author=user)
        template_data = {'posts': all_posts}
        return render(request, 'smain.html', {'method': method,
                                              'user': user,
                                              'posts': all_posts})
    elif request.method == 'POST':
        method = request.method
        uname = request.POST.get('uname')
        psw = request.POST.get('psw')
        user = authenticate(request, username=uname, password=psw)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('smain')
        else:
            return HttpResponse('Username or Password is invalid')


def tmain(request):
    if request.method == 'GET':
        method = request.method
        user = request.user
        return render(request, 'tmain.html', {'method': method,
                                              'user': user})
    elif request.method == 'POST':
        method = request.method
        uname = request.POST.get('uname')
        psw = request.POST.get('psw')
        user = authenticate(request, username=uname, password=psw)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('tmain')
        else:
            return HttpResponse('Username or Password is invalid')


def thread(request):
    method = request.method
    user = request.user
    if user is not None:
        return render(request, 'thread.html', {'method': method,
                                               'user': user})
    else:
        return HttpResponse('Login sesstion is invalid')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            uname = form.cleaned_data.get('username')
            psw = form.cleaned_data.get('password1')
            psw_repeat = form.cleaned_data.get('password2')
            print(psw, psw_repeat)
            if psw != psw_repeat:
                return HttpResponse('password != repeated password')
            user = authenticate(username=uname, password=psw)
            login(request, user)
            return render(request, 'signup.html', {'user': user})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})


def detail(request, question_id):
    question = Question.objects.get(id=question_id)
    return HttpResponse(question.title + question.content)
