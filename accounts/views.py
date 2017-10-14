# coding: utf-8
import json
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.forms import AuthenticationForm
from .forms import RFPAuthForm


def auth_login(request):
    if request.user.is_authenticated():
        return redirect(reverse('tail:tail'))
    if request.method == 'POST':
        form = RFPAuthForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                if user.is_active:
                    login(request, user)
                    data = {'success': True, 'msg': 'success'}
                    #return redirect(reverse('tail:tail'))
                else:
                    data = {'success': False, 'msg': 'User is not active'}
                    #return HttpResponse('Disabled account')
            else:
                data = {'success': False, 'msg': 'Invalid login'}
                #return HttpResponse('Invalid login')
        else:
            data = {'success': False, 'msg': '输入正确的帐号或密码'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        form = RFPAuthForm()
    return render(request, 'accounts/login.html', {'form': form})