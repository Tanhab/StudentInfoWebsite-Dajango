from django.shortcuts import render,redirect

from account.models import Account


# Create your views here.

def home_screen_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {}
    account_list = Account.objects.all();
    context['accounts'] = account_list
    return render(request, "homepage/index.html", context)
