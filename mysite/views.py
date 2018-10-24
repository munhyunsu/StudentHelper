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
        my_reply = Reply.objects.filter(author=user).order_by('-pub_date')
        reply = list()
        for r in my_reply:
            q = Question.objects.get(id=r.to)
            reply.append({'to': r.to,
                          'title': q.title,
                          'pub_date': r.pub_date})
        unsolved_question = Question.objects.filter(is_done=False).order_by('pub_date')
        return render(request, 'tmain.html', {'my_reply': reply,
                                              'questions': unsolved_question})
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
    if request.method == 'POST':
        user = request.user
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = user.username
        pub_date = timezone.now()
        is_done = False
        question = Question(title=title,
                            content=content,
                            author=author,
                            pub_date=pub_date,
                            is_done=is_done)
        question.save()
        return HttpResponseRedirect('/detail/{0}'.format(question.id))
    else:
        return render(request, 'thread.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            uname = form.cleaned_data.get('username')
            psw = form.cleaned_data.get('password1')
            psw_repeat = form.cleaned_data.get('password2')
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
                question = Question.objects.get(id=question_id)
                question.is_done = True
                question.save()
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
