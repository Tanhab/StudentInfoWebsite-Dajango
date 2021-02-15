from django.core.paginator import PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from operator import attrgetter
from account.models import Account


def get_account_queryset(query=None):
    queryset = []
    queries = query.split(" ")  # python install 2019 = [python, install, 2019]
    for q in queries:
        accounts = Account.objects.filter(
            Q(username__icontains=q) |
            Q(reg_num__icontains=q) |
            Q(blood_group__icontains=q) |
            Q(address__icontains=q)

        ).distinct()

        for account in accounts:
            queryset.append(account)

    return list(set(queryset))


# Create your views here.

def home_screen_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {}
    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    account_list = sorted(get_account_queryset(query), key=attrgetter('reg_num'))
    context['accounts'] = account_list
    return render(request, "homepage/index.html", context)


def hall_of_fame_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {}
    return render(request, "homepage/hall_of_fame.html", context)


