from django.shortcuts import render, redirect

#authenticate checks their credientials before logging them into the website
from django.contrib.auth import login, authenticate, logout

from account.forms import AccountAuthenticationForm, RegistrationForm, AccountUpdateForm

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            #checks if the users credientials are correct
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request,account)
            return redirect('home')

        #if the user does not input the correct password or an email then the form is still taken but an error message is displayed
        else:
            context['registration_form'] = form
    
    else: #get request
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)

# when user wants to logout it will bring them to the homepage
def logout_view(request):
    logout(request)
    return redirect('home')


# view of the login url
def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.POST:

        #stores the data the user inputs as form 
        form = AccountAuthenticationForm(request.POST)
        
        #if the form is a valid input of data then it will store what they inputed as an email and password
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            #if the user enters in correct credentials to their account they can login
            if user:
                login(request, user)
                return redirect('home')
            
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'account/login.html', context)
        
def account_view(request):
     
    if not request.user.is_authenticated:
        return redirect('login')
    
    context = {}

    #checks if the user has submitted a request form to change their account details
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        
        #if their form has no errors/conflicts then it will change their account details
        if form.is_valid():
            form.initial = {
                "email":request.POST['email'],
                "username": request.POST['username'],
            }
            form.save()
            context['success_message'] = "Your account details have been updated"
    
    else:
        form = AccountUpdateForm(
            initial = {
                'email': request.user.email,
                'username': request.user.username,
            }
        )
    
    context['account_form'] = form
    return render(request,'account/account.html', context)
