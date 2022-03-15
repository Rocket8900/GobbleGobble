from django import forms 
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm

class PwdResetConfirmForm(SetPasswordForm):
	new_password1 = forms.CharField(
		label='New password', widget=forms.PasswordInput(
			attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
	new_password2 = forms.CharField(
		label='Repeat password', widget=forms.PasswordInput(
			attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))

class PwdChangeForm(PasswordChangeForm):

	old_password = forms.CharField(
		label='Old Password', widget=forms.PasswordInput(
			attrs={'class': 'form-control mb-3', 'placeholder': 'Old Password', 'id': 'form-oldpass'}))
	new_password1 = forms.CharField(
		label='New password', widget=forms.PasswordInput(
			attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
	new_password2 = forms.CharField(
		label='Repeat password', widget=forms.PasswordInput(
			attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))

class PwdResetForm(PasswordResetForm):
	email = forms.EmailField(max_length=254, widget=forms.TextInput(
		attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

# LOOK INTO REMOVING THIS SECTION FOR SECURITY REASONS
	def clean_email(self):
		email = self.cleaned_data['email']
		test = User.objects.filter(email=email)
		if not test:
			raise forms.ValidationError(
				'Unfortunatley we can not find that email address')
		return email

class UserLoginForm(AuthenticationForm):
	username = forms.CharField(widget=forms.TextInput(
		attrs={
			'class': 'form-control mb-3',
			'placeholder':'Username',
			'id':'login-username',
		}))
	password = forms.CharField(widget=forms.PasswordInput(
		attrs={
			'class': 'form-control',
			'placeholder':'Password',
			'id':'login-pwd',
		}))

class RegistrationForm(forms.ModelForm):

	username = forms.CharField(
		label = "enter username", min_length=4, max_length=50, help_text='required')
	email = forms.EmailField(
		max_length=100, help_text='required', error_messages={'required':'input a valid email'})
	password = forms.CharField(label='password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='repeat password', widget=forms.PasswordInput)

	class Meta:
		model = User 
		# Model has been imported allowing us to access the attributes for filtering
		fields = ('username', 'email', 'first_name')

	def clean_username(self):
		username = self.cleaned_data['username'].lower()
		r = User.objects.filter(username=username)
		if r.count():
			raise ValidationError('Username Already Exists')

		return username

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise ValidationError('Passwords dont match')
		return cd['password2']

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('That email is already registered, please use another')
		return email

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update(
			{'class': 'form-control mb-3', 'placeholder': 'Username'})
		self.fields['email'].widget.attrs.update(
			{'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
		self.fields['password'].widget.attrs.update(
			{'class': 'form-control', 'placeholder': 'Password'})
		self.fields['password2'].widget.attrs.update(
			{'class': 'form-control', 'placeholder': 'Repeat Password'})

class UserEditForm(forms.ModelForm):

	first_name = forms.CharField(
		label='Firstname', min_length=4, max_length=50, widget=forms.TextInput(
			attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-firstname'}))

	last_name = forms.CharField(
		label='Lastname', min_length=4, max_length=50, widget=forms.TextInput(
			attrs={'class': 'form-control mb-3', 'placeholder': 'Lastname', 'id': 'form-lastname'}))

	email = forms.EmailField(
		max_length=200, widget=forms.TextInput(
			attrs={'class': 'form-control mb-3', 'placeholder': 'Old Password', 'id': 'form-email'}))

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError(
				'Please use another Email, that is already taken')
		return email

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['last_name'].required = False
		self.fields['email'].required = False