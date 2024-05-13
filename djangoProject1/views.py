from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from djangoProject1.models import Account, gen_code
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from .models import CustomUser as User
from .forms import AvatarForm


def index(request):
    if request.method == 'POST':
        # Получаем данные из формы
        email = request.POST.get('email')
        login = request.POST.get('login')
        password = request.POST.get('password')
        name = request.POST.get('name')
        surname = request.POST.get('surname')

        # Проверяем, существует ли пользователь с таким именем пользователя
        if User.objects.filter(username=login).exists():
            messages.error(request, "Пользователь с таким именем уже существует")
            return redirect('index')

        # Создаем объект User
        user = User.objects.create_user(username=login, email=email, password=password, first_name=name,last_name=surname)
        acc = Account.objects.create(login=login, email=email, password=password, bonuces=1, t2=False,name=name, surname=surname)

        # Перенаправляем на страницу успешной регистрации
        return redirect('login')
    else:
        return render(request, 'index.html')


def success(request):
    return render(request, 'success.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('login1')
        password = request.POST.get('password1')

        # Проверяем существует ли пользователь с таким именем пользователя
        user = User.objects.filter(username=username).first()
        acc = Account.objects.filter(login=username).first()

        if user is not None:
            # Проверяем введенный пароль
            if user.check_password(password):
                if acc.t2 == True:
                    auth_login(request, user)
                    code = gen_code(user.email)
                    request.session['email_code'] = code
                    return redirect('auth')

                # Аутентифицируем пользователя
                auth_login(request, user)
                return redirect('account')
                # return render(request, 'personal_account.html')
            else:
                # Пароль неверный
                messages.error(request, "Неправильный пароль")
        else:
            # Пользователь с таким именем не найден
            messages.error(request, "Пользователь с таким именем не найден")

        return redirect('login')

    else:
        return render(request, 'login.html')


@login_required()
def account(request):
    user = request.user

    old_pass = request.POST.get('old_pass')
    new_pass = request.POST.get('new_pass')
    re_pass = request.POST.get('re_pass')

    # Получаем объект Account текущего пользователя
    obj = Account.objects.filter(login=user.username).first()

    # Если объект не найден, создаем новый с начальным значением bonuces
    if obj is None:
        obj = Account.objects.create(login=user.username, bonuces=0)

    form = AvatarForm()  # Объявляем form здесь

    if request.method == 'POST':


        if 'farm' in request.POST:
            obj.bonuces += 1
            obj.save()
        elif 'auth' in request.POST:
            if obj.t2 == False:
                obj.t2 = True
            else:
                obj.t2 = False
            obj.save()
            return redirect('account')
        elif 'exit' in request.POST:
            return redirect('/')
        elif 'change_email' in request.POST:
            return redirect('change_email1')
        elif 'upload_avatar' in request.POST:
            form = AvatarForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                user_profile = form.save(commit=False)
                user_profile.user = request.user
                user_profile.save()
                return redirect('account')
    form = AvatarForm(instance=user)
    user_data = {
        'username': user.username,
        'surname': user.last_name,
        'email': user.email,
        'bonuses': obj.bonuces,
        "t2": obj.t2,
        'form': form,
        'name': user.first_name
    }
    print(f"хуц йуцуц {user_data['form']}")

    return render(request, 'personal_account.html', {'user_data': user_data})


def auth(request):
    if request.method == 'POST':
        code = request.POST.get('code')

        tr_code = request.session.get('email_code')

        if str(code) == str(tr_code):
            return redirect('account')
        else:
            error_occurred = True
            # return redirect('auth')
            return render(request, 'auth.html', {'error_occurred': error_occurred})

    else:
        return render(request, 'auth.html')


def change_password(request):
    if request.method == 'POST':
        email = request.POST.get('input_email')
        user = User.objects.filter(email=email).first()
        if user:
            request.session['email'] = email
            return redirect('change_password2')
        else:
            error_occurred = True
            return render(request, 'change_password.html', {'error_occurred': error_occurred})
    else:
        return render(request, 'change_password.html')


def change_password2(request):
    if request.method == 'POST':
        email = request.session.get('email')
        new_password = request.POST.get('new_pass')
        re_password = request.POST.get('re_pass')

        if new_password == re_password:
            # Update password in User model
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)

                Account.objects.filter(email=email).update(password=new_password)
                return redirect('login')
            except User.DoesNotExist:
                pass
        else:
            error_occ = True
            return render(request, 'change_password2.html', {'error_occurred': error_occ})
    else:
        return render(request, 'change_password2.html')


def change_email1(request):
    if request.method == 'POST':
        password = request.POST.get('confirm_pass')

        if request.user.is_authenticated:
            tr_password = User.objects.get(id=request.user.id)
            passa = tr_password.password
            email = tr_password.email
            print(passa)
            print(password)
            if check_password(password, passa):
                code = gen_code(email)
                request.session['code_email'] = code
                return redirect('change_email2')
            else:
                return render(request, 'change_email1.html')

    return render(request, 'change_email1.html')


def change_email2(request):
    if request.method == 'POST':
        code = request.session.get('code_email')  # Получаем код из сессии
        user_code = request.POST.get('confirm_email')

        if str(user_code) == str(code):
            return redirect('change_email3')
        else:
            print(user_code)
            print(code)
            return render(request, 'change_email2.html')

    return render(request, 'change_email2.html')


@login_required
def change_email3(request):
    if request.method == 'POST':
        new_email = request.POST.get('input_email')

        # Проверка на корректность нового адреса электронной почты
        if not new_email:
            return render(request, 'change_email3.html', {'error_message': 'Please provide a valid email address.'})

        Account.objects.filter(id=request.user.id).update(email=new_email)
        request.user.email = new_email
        request.user.save()
        success = True
        # Перенаправление на страницу с профилем или другую страницу
        return redirect('account')

    # В случае GET-запроса просто отображаем форму для смены email
    return render(request, 'change_email3.html')
