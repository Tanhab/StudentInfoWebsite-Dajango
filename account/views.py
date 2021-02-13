from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
# from blog.models import BlogPost

from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from account.models import Account


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST or None, request.FILES or None)
        # is valid check if the inputs are all correct
        if form.is_valid():
            account = form.save()
            account.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=raw_password)
            login(request, account)
            return redirect('home')
        else:  # Not correct input for form, so keep those data and show error
            context['registration_form'] = form

    else:  # GET request - create a black form
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect("home")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    # print(form)
    return render(request, "account/login.html", context)


def account_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            form.initial = {
                "username": request.POST['username'],
                "phone_number": request.POST['phone_number'],
                "blood_group": request.POST['blood_group'],
                "address": request.POST['address'],
                "image": obj.image,
                "reg_num": request.POST['reg_num'],
                'email': request.POST['email'],
            }

            # form.save()
            context['success_message'] = "Updated"
            context['account_form'] = form
    else:
        account = get_object_or_404(Account, pk=request.user.pk)

        form = AccountUpdateForm(
            initial={

                "username": request.user.username,
                "phone_number": account.phone_number,
                "blood_group": account.blood_group,
                "address": account.address,
                "image": account.image,
                "reg_num":account.reg_num,
                'email': account.email,

            }
        )

    context['account_form'] = form

    # blog_posts = BlogPost.objects.filter(author=request.user)
    # context['blog_posts'] = blog_posts
    return render(request, "account/account.html", context)


def must_authenticate_view(request):
    return render(request, 'account/must_authenticate.html', {})
