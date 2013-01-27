from __future__ import absolute_import

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from permissions.models import Permission

from .conf.settings import DISABLE_HOME_VIEW


def home(request):
    if DISABLE_HOME_VIEW:
        return HttpResponseRedirect(reverse('document_list_recent'))
    else:
        return render_to_response('home.html', {},
        context_instance=RequestContext(request))
