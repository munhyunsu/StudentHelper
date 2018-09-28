from django.http import HttpResponse
from django.template import loader


def index(request):
    id = request.GET.get('identifier')
    passwd = request.GET.get('password')
    mem_type = request.GET.get('member_type')
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'id': id,
                                         'passwd': passwd,
                                         'mem_type': mem_type}))