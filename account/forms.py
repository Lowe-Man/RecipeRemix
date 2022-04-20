from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import modelformset_factory

from account.models import Allergy, Pantry

Account = get_user_model()


class RegistrationForm(UserCreationForm):
	username = forms.CharField(
		label="Username",
		widget=forms.TextInput(
			attrs={"class": "form-control"}
		)
	)
	email = forms.EmailField(
		label="Email",
		max_length=60,
		widget=forms.EmailInput(
			attrs={"class": "form-control"}
		)
	)
	password1 = forms.CharField(
		label="Password",
		widget=forms.PasswordInput(
			attrs={"class": "form-control"}
		)
	)
	password2 = forms.CharField(
		label="Password Confirm",
		widget=forms.PasswordInput(
			attrs={"class": "form-control"}
		)
	)

	def clean_username(self):
		username = self.cleaned_data.get("username")
		qs = Account.objects.filter(username__iexact=username)
		if qs.exists():
			raise forms.ValidationError("This is an invalid username, please pick another one.")
		return username

	def clean_email(self):
		email = self.cleaned_data.get("email")
		qs = Account.objects.filter(email__iexact=email)
		if qs.exists():
			raise forms.ValidationError("This email is already in use.")
		return email

	class Meta(UserCreationForm.Meta):
		model = Account
		fields = ("username", "email", "password1", "password2")


class AccountAuthenticationForm(forms.ModelForm):
	email = forms.EmailField(
		label="Email",
		max_length=60,
		widget=forms.EmailInput(
			attrs={"class": "form-control", "name": "email"}
		)
	)
	password = forms.CharField(
		label="Password",
		widget=forms.PasswordInput(
			attrs={"class": "form-control", "name": "password"}
		)
	)

	class Meta:
		model = Account
		fields = ("email", "password")

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data.get("email")
			password = self.cleaned_data.get("password")
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")


# This class is a for that update allergies according to the list the api uses
class AllergyUpdateForm(forms.ModelForm):
	options = (
		("1", "Select"),
		("2", "Dairy"),
		("3", "Egg"),
		("4", "Gluten"),
		("5", "Grain"),
		("6", "Peanut"),
		("7", "Seafood"),
		("8", "Sesame"),
		("9", "Shellfish"),
		("10", "Soy"),
		("11", "Sulfite"),
		("12", "Trea Nut"),
		("13", "Wheat")
	)

	item = forms.CharField(
		label="Allergy",
		widget=forms.Select(
			attrs={"class": "form-control"},
			choices=options
		)

	)
	print(item)

	class Meta:
		model = Allergy
		fields = ["item"]


AllergyUpdateFormSet = modelformset_factory(
	Allergy, fields=("item",), extra=0, form=AllergyUpdateForm, can_delete=True
)


class PantryUpdateForm(forms.ModelForm):
	item = forms.CharField(
		label="Pantry",
		widget=forms.TextInput(
			attrs={"class": "form-control"}
		)
	)

	class Meta:
		model = Pantry
		fields = ["item"]


PantryUpdateFormSet = modelformset_factory(
	Pantry, fields=("item",), extra=0, form=PantryUpdateForm, can_delete=True
)
