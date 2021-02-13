from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account, blood_group_options


class RegistrationForm(UserCreationForm):
    reg_num = forms.IntegerField(required=True)
    email = forms.EmailField(required=False)
    phone_number = forms.IntegerField(required=False)
    address = forms.CharField(max_length=100, required=False)
    image = forms.ImageField(required=False)
    blood_group = forms.ChoiceField(choices=blood_group_options,widget=forms.Select(attrs={'class': 'form_control'}))

    class Meta:
        model = Account
        fields = ('username', 'reg_num', 'password1', 'password2', 'blood_group', 'address', 'image',
                  'phone_number', 'email')


# using custom Modelform to make our login form


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('username', 'password')

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("Invalid login")


class AccountUpdateForm(forms.ModelForm):
    blood_group = forms.ChoiceField(choices=blood_group_options,widget=forms.Select(attrs={'class': 'form_control'}))

    class Meta:
        model = Account
        fields = ('username', 'phone_number', 'blood_group', 'address', 'image', 'reg_num', 'email')

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     try:
    #         account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
    #     except Account.DoesNotExist:
    #         return email
    #     raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)

    def clean_reg_num(self):
        reg_num = self.cleaned_data['reg_num']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(reg_num=reg_num)
        except Account.DoesNotExist:
            return reg_num
        raise forms.ValidationError('Registration number "%d" is already in use.' % reg_num)

    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        return phone_number

    def clean_address(self):
        address = self.cleaned_data['address']
        return address

    def clean_blood_group(self):
        blood_group = self.cleaned_data['blood_group']
        return blood_group

    def clean_image(self):
        image = self.cleaned_data['image']
        return image

    def save(self, commit=True):
        account = self.instance
        account.username = self.cleaned_data['username']
        account.blood_group = self.cleaned_data['blood_group']
        account.address = self.cleaned_data['address']
        account.phone_number = self.cleaned_data['phone_number']

        if self.cleaned_data['image']:
            account.image = self.cleaned_data['image']

        if commit:
            account.save()
        return account
