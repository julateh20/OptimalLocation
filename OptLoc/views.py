import json

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages  # import messages
from django.contrib.auth.forms import AuthenticationForm  # add this
from OptLoc.forms import OptLocForm, NewUserForm
from OptLoc.optimalLocation import OptimalLocationModel
import pandas as pd

# Create your views here.
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def index(request):
    # Backend process
    # [City, optLoc] = OptimalLocationModel.CalculateOptimalLocation(1001)
    City = ''
    Coords = ''

    if request.method == 'POST':
        form = OptLocForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            region = form.cleaned_data['region']

            print(region)
            if region == 'Dalarna' or region == 'dalarna':
                csv_path = 'C:\\OptimalLocation\\Dalarna.csv'
                # Load the Pandas Dataframe of the Borlange Population grid
                df = pd.read_csv(csv_path, delimiter=',')

                # print(df)
                optLoc = OptimalLocationModel(df, p=1)
                location = optLoc.find()

                print('Optimal location(s) for store: ')
                print([df['NAMN_'][i] for i in location['Allocation']])

                City = df['NAMN_'][location['Allocation'][0]]
                Coords = [df['X'][location['Allocation'][0]], df['Y'][location['Allocation'][0]]]
            else:
                Coords = 'NotFound'
        else:
            form = OptLocForm()
    else:
        form = OptLocForm()
    # You can access database - GEODjango
    # Display result - optimal location
    return render(request, 'OptLoc.html',
                  {'form': form, 'Optimal_Location': Coords,
                   'Optimal_City': City})


# Register
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.error(request, "successful registration.")
            return redirect("homepage")
        else:
            # for msg in form.error_messages:
            #   messages.error(request, f"{msg}: {form.error_messages[msg]}")
            #   print(msg)
            password1 = form.data['password1']
            password2 = form.data['password2']
            email = form.data['email']
            for msg in form.errors.as_data():
                if msg == 'email':
                    messages.error(request, "Declared {email} is not valid")
                if msg == 'password2' and password1 == password2:
                    messages.error(request, "Selected password: {password1} is not strong enough")
                elif msg == 'password2' and password1 != password2:
                    messages.error(request, "Password: '{password1}' and Confirmation Password: '{password2}' do not match")
            print("Unsuccessful registration. Invalid information.")
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")

    return redirect("homepage")
