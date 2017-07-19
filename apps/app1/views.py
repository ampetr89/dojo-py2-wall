from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Message, Comment
from django.forms.models import model_to_dict

def check_login(request):
    if 'logged_in' in request.session:
        return request.session['logged_in']
    else:
        return False

# /
def index(request):
    request.session['logged_in'] = check_login(request)    
    if request.session['logged_in']:
        return redirect('/wall')
    else:
        return redirect('/login')

# /wall
def wall(request):
    request.session['logged_in'] = check_login(request)
    if request.session['logged_in']:
        return render(request, 'app1/wall.html')
    else:
        return redirect('/login')

# /login
def login(request):
    request.session['logged_in'] = check_login(request)
    if not request.session['logged_in']:
        return render(request, 'app1/login.html')
    else:
        return redirect('/wall')
   
# /register
def register(request):
    request.session['logged_in'] = check_login(request)
    if not request.session['logged_in']:
        return render(request, 'app1/register.html')
    else:
        return redirect('/wall')

def flash(request, message_type, message_list):
    print(message_type)
    print(message_list)
    for msg_text in message_list:
        messages.add_message(request, message_type, msg_text)
    
def process_login(request):
    if request.method=='GET':
        return redirect('/')
    else:
        data= request.POST
        test_user = User(
            email= data['email'],
            password = data['password']
            )
        login_errors = test_user.login_errors()
        if len(login_errors) > 0:
            print('errors in log in')
            print(' - '.join(login_errors))
            flash(request, messages.ERROR, login_errors)
            return redirect('/login')
        else:
            request.session['logged_in'] = True
            return redirect('/')

def process_registration(request):
    if request.method=='GET':
        return redirect('/')
    else:
        data = request.POST

        test_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password'],)
        reg_errors = test_user.registration_errors()

        # check password == password2
        if data['password'] != data['password2']:
            reg_errors.append('Passwords must match.')

        if reg_errors:
            print('errors in registration')
            print(' - '.join(reg_errors))
            flash(request, messages.ERROR, reg_errors)
            return redirect('/register')
        else:
            User.objects.create(**model_to_dict(test_user))
            print('user added successfully')
            flash(request, messages.INFO, ['Registration successful! You may now log in.'])
            return redirect('/login')

# /logout
def logout(request):
    try:
        # the logout button will send a post request. this should be the only way to log out
        request.POST['logout']
        request.session['logged_in'] = False
        return render(request, 'app1/login.html')
    except:
        return redirect('/wall')

# /get-content
def get_content(request):
    pass