from django.shortcuts import render
from django import template
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.conf import settings
import os
#from portal.models import Forms
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.template.loader import get_template
from django.middleware.csrf import get_token

import string
import random
import datetime
import requests


class HomePage(TemplateView):
    # preperation to replace old homepage with screen designs..

    template_name = 'home_page.html'
    def render_to_response(self, context):

        #if self.request.user.is_authenticated:
        #   if len(self.request.user.first_name) > 0:
        #       donothing = ''
        #   else:
        #       return HttpResponseRedirect(reverse('first_login_info_steps', args=(self.request.user.id,1)))
        template = get_template(self.template_name)
        #context = RequestContext(self.request)
        context['request'] = self.request
        context['csrf_token_value'] = get_token(self.request)
        context['sso_auth_session_id'] = self.request.COOKIES.get('sso_auth_session_id','')
        context['referer'] = self.request.GET.get('referer',None)
        return HttpResponse(template.render(context))

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['request'] = self.request
        context['user'] = self.request.user
        if self.request.user.is_staff is True:
           context['staff'] = self.request.user.is_staff
        else:
           context['staff'] = False

        #context = template_context(self.request)
        return context


def CheckAuth(request):
     text = request.COOKIES.get('session','')
     cookie_session = request.COOKIES.get('sso_auth_session_id','')
     get_session = request.GET.get('sso_auth_session_id',None)
     referer = request.GET.get('referer','')

     session_id = None
     if get_session:
           session_id = get_session


     if request.user.is_authenticated:
         response = HttpResponse('Authenticated', content_type='text/plain', status=200)
         response['X-TestUser'] = 'jason@austwa.comiii'
         if get_session:
               response.set_cookie('sso_auth_session_id', get_session, max_age=sess.expiry,expires=sess.expiry)
               response = HttpResponseRedirect(referer)
     else:
         response = HttpResponse('Unable to find valid session', content_type='text/plain', status=403)
     return response


# Session Verification
def Auth(request):
     text = request.COOKIES.get('session','')
     cookie_session = request.COOKIES.get('sso_auth_session_id','')
     get_session = request.GET.get('sso_auth_session_id',None)
     referer = request.GET.get('referer','')

     session_id = None
     if get_session:
           session_id = get_session
           response = HttpResponse('session cookie saved<script>window.location.href="'+referer+'";</script>', content_type='text/html', status=200)
           response.set_cookie('sso_auth_session_id', get_session )

           #response = HttpResponseRedirect(referer)
           return response
     else:
           session_id = cookie_session

     if request.user.is_authenticated: 
         response = HttpResponse('Authenticated', content_type='text/plain', status=200)
        
         response['X-TestUser'] = 'jason@austwa.comiii'
         response['X-REMOTEUSER'] = request.user.email 
         response['X-LASTNAME'] = request.user.last_name
         response['X-FIRSTNAME'] = request.user.first_name
         response['X-EMAIL'] = request.user.email 

         if get_session:
               response.set_cookie('sso_auth_session_id', get_session )
               response = HttpResponseRedirect(referer)
     else:
         response = HttpResponse('Unable to find valid session', content_type='text/plain', status=403)
     return response


from django.contrib.auth import logout

def sso_logout(request):
    your_data = request.session.get('your_key', None)
    current_expiry = request.session.get('_session_expiry')
    logout(request)
    if your_data:
        request.session[settings.SESSION_COOKIE_NAME] = your_data
        if current_expiry:
           request.session['_session_expiry'] = current_expiry
    response = HttpResponse('<script>window.location="/";</script>', content_type='text/html', status=200)
    return response

def logout_old(request):
    """
    Removes the authenticated user's ID from the request and flushes their
    session data.
    """
    # Dispatch the signal before the user is logged out so the receivers have a
    # chance to find out *who* logged out.
    user = getattr(request, 'user', None)
    if hasattr(user, 'is_authenticated') and not user.is_authenticated():
        user = None
    user_logged_out.send(sender=user.__class__, request=request, user=user)

    request.session.flush()
    if hasattr(request, 'user'):
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()




     #session_id = None
     #if get_session:
     #    session_id = get_session
     #else:
     #    session_id = cookie_session
     #request.headers['X-TestUser'] = 'jason@austwa.com'

#     if models.SMSSession.objects.filter(session=session_id, expiry__gte=datetime.datetime.now()).count() > 0:
#         sess = models.SMSSession.objects.filter(session=session_id)[0]
#         response = HttpResponse(text, content_type='text/plain', status=200)
#         response['X-TestUser'] = 'jason@austwa.comiii'
#         if get_session:
#             response = HttpResponseRedirect(referer)
#             response.set_cookie('sso_auth_session_id', get_session, max_age=sess.expiry,expires=sess.expiry)
#     else:
#         response = HttpResponse('Unable to find valid session', content_type='text/plain', status=403)
#     return response
#


