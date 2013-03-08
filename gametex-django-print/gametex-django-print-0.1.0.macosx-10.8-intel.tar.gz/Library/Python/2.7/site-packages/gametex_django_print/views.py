# Create your views here.
from cStringIO import StringIO
from django.http import HttpResponse
from gametex.models import GTO
from gametex_django_print.obfuscate import deobfuscate
from latex import pdflatex
from traceback import print_exc
from django.conf import settings

def pdf(request):
    try:
        obf = request.GET.get('o', 0)
        items = request.GET.get('items', None)
        gtc = request.GET.get('gtc', None)
        if not gtc and items:
            return HttpResponse("You must include both 'items' and 'gtc' in your get params.")
        if obf:
            items = deobfuscate(items, settings.OBFUSCATE_KEY)
            gtc = deobfuscate(gtc, settings.OBFUSCATE_KEY)
        items = items.split(',')
        owner = request.GET.get('owner', None)
        fname = pdflatex(items, gtc, owner=owner)
        if fname:
            data = open(fname, 'r').read()
            response = HttpResponse(data, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="consortium.pdf"'
            return response
        else:
            return HttpResponse("Something went wrong there!")
    except Exception as e:
        buf = StringIO()
        print_exc(e, file=buf)
        return HttpResponse("Whoops! %s" % buf.getvalue())