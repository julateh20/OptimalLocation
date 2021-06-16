from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class OptLocForm(forms.Form):
    region = forms.CharField(label='Region name')
    retailerName = forms.CharField(label='Retailer name')
    storeName = forms.CharField(label='Store name')


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields =		 ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		print('Émail : ' + user.email)
		if commit:
			user.save()
		return user
