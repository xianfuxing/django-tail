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
                    return redirect(reverse('tail:tail'))
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = RFPAuthForm()
    return render(request, 'accounts/login.html', {'form': form})
