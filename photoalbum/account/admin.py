from django import forms
from django.forms import extras
from account.models import Account
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Button, Submit
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

class RegistrationForm(forms.ModelForm):
  
  #TODO: email regex here!

  error_messages = {
    'duplicate_email': "A user with that email already exists.",
    'password_mismatch': "The two password fields didn't match.",
  }

  password1 = forms.CharField(
    label="Password",
    widget=forms.PasswordInput
  )
  password2 = forms.CharField(
    label="Password confirmation",
    widget=forms.PasswordInput,
    help_text="Enter the same password as above, for verification."
  )
  
  class Meta:
    model = Account
    widgets = {
      'date_of_birth': extras.SelectDateWidget(years=range(1920, 2008)),
      'gender': forms.RadioSelect(),
    }
    fields = (
        'firstname', 'lastname', 'email', 'date_of_birth', 'gender',
    )
  
  def __init__(self, *args, **kwargs):
    super(RegistrationForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.layout = Layout(
      Field('firstname', placeholder="First name"),
      Field('lastname', placeholder="Last name"),
      Field('email', placeholder="Email"),
      Field('password1', placeholder="Password"),
      Field('password2', placeholder="Password confirmation"),
      Field('date_of_birth', placeholder="Date of birth"),
      Field('gender'),
      FormActions(
        Submit('save', 'Submit', css_class="btn-register"),
        Submit('cancel', 'Cancel'),
      ),
    )
    self.helper.form_show_labels = False
  
  def clean_username(self):
    username = self.cleaned_data["email"]
    try:
      Account._default_manager.get(username=username)
    except Account.DoesNotExist:
      return username
    raise forms.ValidationError(
      self.error_messages['duplicate_username'],
      code='duplicate_username',
    )

  def clean_password2(self): #Verify that the passwords match
    password1 = self.cleaned_data.get("password1")
    password2 = self.cleaned_data.get("password2")
    if password1 and password2 and password1 != password2:
      raise forms.ValidationError(
          self.error_messages['password_mismatch'],
          code='password_mismatch',
      )
    return password2

  def save(self, commit=True):
    # Save the provided password as a hash
    user = super(RegistrationForm, self).save(commit=False)
    user.set_password(self.cleaned_data["password1"])
    if commit:
      user.save()
    return user

class LoginForm(AuthenticationForm): #Extend the AuthenticationForm with crispy forms
  def __init__(self, *args, **kwargs):
    super(LoginForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.layout = Layout(
      Field('username', placeholder="email"),
      Field('password', placeholder="password"),
      FormActions(
        Submit('login', 'Log in', css_class="btn-login"),
        Submit('cancel', 'Cancel'),
      ),
    )
    self.helper.form_show_labels = False
