#!/bin/sh

project_name="d06"
app_name="ex"
settings_file="$project_name/settings.py"
views_file="$app_name/views.py"
app_urls_file="$app_name/urls.py"
app_forms_file="$app_name/forms.py"
project_urls_file="$project_name/urls.py"
app_models_file="$app_name/models.py"
templates_dir_app="$app_name/templates/$app_name"
templates_files="../templates/$app_name/base.html  ../templates/$app_name/nav.html"



# Change to the project directory.
cd "$project_name"


# Create a Django app in the project.
python manage.py startapp "$app_name"
echo "✅ $app_name APP created."


# Add the app to the INSTALLED_APPS list in the settings.py file of the project.
sed -i "/INSTALLED_APPS = \[/,/]/ s/\(]\)/    '$app_name',\n&/" "$settings_file"
echo "✅ $app_name added to INSTALLED_APPS."


# Create a view in the views.py file of the app.
cat << 'EOL' >> "$views_file"
from django.shortcuts import render, HttpResponse, redirect
from django.conf import settings
import random
from .forms import SignupForm, LoginForm, TipForm
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Tip, Upvote, Downvote
from django.forms.models import model_to_dict


def home(request):
    tips = Tip.objects.all().order_by('date')
    if request.method == 'POST':
        if 'deletetip' in request.POST:
            # print("removal request for a tip")
            if (request.user.has_perm('ex.deletetip') or
                    model_to_dict(Tip.objects.get(
                        id=request.POST['tipid'])).get('auteur') ==
                    request.user.username):
                form = TipForm()
                t = Tip.objects.filter(id=request.POST['tipid'])
                t.delete()
        elif 'upvote' in request.POST:
            # print("upvote request")
            form = TipForm()
            ts = Tip.objects.filter(id=request.POST['tipid'])
            if len(ts) > 0:
                t = ts[0]
                t.upvoteForUser(request.user.username)
        elif 'downvote' in request.POST:
            # print("downvote request")
            form = TipForm()
            ts = Tip.objects.filter(id=request.POST['tipid'])
            if len(ts) > 0:
                t = ts[0]
                t.downvoteForUser(request.user.username)
        else:
            form = TipForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                tip = Tip(content=data['content'], auteur=request.user.username)
                tip.save()
                # print('New Tip Created',tip)
            #return redirect('/')
    else: # method 'GET':
        # print("method 'GET':form = TipForm()")
        form = TipForm()
    if request.COOKIES.get('mycookie'):
        # print("if request.COOKIES.get('mycookie')")
        usador = request.COOKIES['mycookie']
        response = render(request, 'ex/index.html', {'usador': usador, 'tips': tips, 'form': form})
    else:
        # print("else: ...request.COOKIES.get('mycookie')")
        usador = random.choice(settings.USER_NAMES)
        response = render(request, 'ex/index.html', {'usador': usador, 'tips': tips, 'form': form})
        response.set_cookie('mycookie', usador, max_age=settings.SESSION_COOKIE_DURATION)

    return response


def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            u = auth.authenticate(username=data['username'], password=data['password'])
            if u and u.is_active:
                auth.login(request, u)
                print('User logged in')
                return redirect('/')
            else:
                print('Unknown or inactive user')
                form._errors['username'] = ['Unknown or inactive user']
    else: # method 'GET':
        print("method 'GET': form = LoginForm()")
        form = LoginForm()

    return render(request, 'ex/login.html', {'usador': request.user, 'form': form, })

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            u = User.objects.create_user(username=data['username'], password=data['password'])
            u.save()
            auth.login(request, u)
            # print('User created and logged in ', u)

            return redirect('/')
    else: # method 'GET':
        # print("method 'GET': form = SignupForm()")
        form = SignupForm()

    return render(request, 'ex/signup.html', {'usador': request.user, 'form': form, })


def logout(request):
    auth.logout(request)
    return redirect('/')

EOL
echo "✅ VIEWS created in $views_file."


# Create a URL pattern in the urls.py file of the app.
cat << 'EOL' >> "$app_urls_file"
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('login/', views.login),
	path('signup/', views.signup),
	path('logout/', views.logout),
]

EOL
echo "✅ URL pattern created in $app_urls_file."


# Create the forms.py file to the app.
cat << 'EOL' >> "$app_forms_file"
from django import forms
from django.contrib.auth.models import User
from .models import Tip

class SignupForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput, initial='')
	verif_password = forms.CharField(required=True, widget=forms.PasswordInput, initial='')
	def clean(self):
		form_data = super(SignupForm, self).clean()
		u = User.objects.filter(username=form_data['username'])
		if len(u) > 0:
			self._errors['username'] = ["The name entered is already taken"]
		if form_data['password'] != form_data['verif_password']:
			self._errors['password'] = ["The password must be identical in the 2 password fields"]
		return form_data


class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput, initial='')


class TipForm(forms.ModelForm):
	class Meta:
		model = Tip
		fields = ['content']

EOL
echo "✅ FORMS file created in $app_forms_file."



# Create models in the models.py file of the app
cat << 'EOL' > "$app_models_file"
from django.db import models
from django.contrib.auth.models import User


class Upvote(models.Model):
    voted_user = models.CharField(max_length=150)


class Downvote(models.Model):
    voted_user = models.CharField(max_length=150)


class Tip(models.Model):
    content = models.TextField()
    auteur = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    upvote = models.ManyToManyField(Upvote)
    downvote = models.ManyToManyField(Downvote)

    def upvoteForUser(self, username):
        votes = self.upvote.all()
        found = False
        for index in votes:
            if index.voted_user == username:
                found = True
                index.delete()
                break
        if not found:
            newvote = Upvote(voted_user=username)
            newvote.save()
            self.upvote.add(newvote)

            downvotes = self.downvote.all()
            for index in downvotes:
                if index.voted_user == username:
                    index.delete()
                    break
            self.save()

    def downvoteForUser(self, username):
        votes = self.downvote.all()
        found = False
        for index in votes:
            if index.voted_user == username:
                found = True
                index.delete()
                break
        if not found:
            newvote = Downvote(voted_user=username)
            newvote.save()
            self.downvote.add(newvote)

            upvotes = self.upvote.all()
            for index in upvotes:
                if index.voted_user == username:
                    index.delete()
                    break
            self.save()

    def __str__(self):
        return str(self.date.strftime('%Y-%m-%d %H:%M:%S')) + ' ' + self.content + ' by ' + self.auteur \
               + ' upvotes : ' + str(len(self.upvote.all())) \
               + ' downvotes : ' + str(len(self.downvote.all()))

    def get_auteur(self):
        return self.auteur


EOL
echo "✅ MODELS created in $app_models_file."


# Create a URL pattern in the urls.py file of the project.
sed -i "1i\\from django.urls.conf import include" "$project_urls_file"

NEW_URL="path('', include('$app_name.urls')),"
sed -i "/urlpatterns = \[/,/]/ s|]|    $NEW_URL\n]|" "$project_urls_file"

echo "✅ URL pattern created in $project_urls_file."



# Create templates in the templates directory of the app.
mkdir -p "$templates_dir_app"
cp $templates_files "$templates_dir_app/"
echo "✅ TEMPLATES created in $templates_dir_app."


echo -e "\n**********************\n"
