from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.utils import timezone

from advice.models import Question, Reply

def index(request):
    return render(request, 'index.html')


def smain(request):
    if request.method == 'GET':
        method = request.method
        user = request.user
        all_posts = Question.objects.all().filter(author=user).order_by('-pub_date')
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
    if request.method == 'POST':
        user = request.user
        locate = request.POST.get('locate')
        if locate == 'question':
            title = request.POST.get('title')
            content = request.POST.get('content')
            question = Question.objects.get(id=question_id)
            question.title = title
            question.content = content
            question.save()
        elif locate == 'reply':
            reply_id = request.POST.get('reply_id')
            content = request.POST.get('content')
            is_selected = request.POST.get('select')
            if is_selected is not None:
                is_selected = True
                replies = Reply.objects.filter(to=question_id)
                for reply in replies:
                    reply.is_selected = False
                    reply.save()
                reply = Reply.objects.get(id=reply_id)
                reply.is_selected = is_selected
                reply.save()
            reply = Reply.objects.get(id=reply_id)
            reply.content = content
            reply.save()
        elif locate == 'new_reply':
            author = request.user.username
            to = question_id
            content = request.POST.get('content')
            pub_date = timezone.now()
            is_selected = False
            reply = Reply(author=author,
                          to=to,
                          content=content,
                          pub_date=pub_date,
                          is_selected=is_selected)
            reply.save()
        return HttpResponseRedirect(request.get_raw_uri())
    else:
        user = request.user
        question = Question.objects.get(id=question_id)
        reply = Reply.objects.filter(to=question_id).order_by('-is_selected', 'pub_date')
        return render(request, 'detail.html', {'user': user,
                                               'question': question,
                                               'reply': reply})
