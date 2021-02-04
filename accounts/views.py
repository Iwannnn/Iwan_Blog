from django.shortcuts import render, redirect, HttpResponse
from .forms import LoginForm, RegisterForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import ProfileForm
from .models import Profile
# Create your views here.


def user_login(request):
    if request.method == 'GET':
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    if request.user.is_authenticated:
        messages.add_message(request, messages.SUCCESS,
                             '您已登录', extra_tags='success')
        return redirect("/")
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            try:
                user = User.objects.get(username=data['username'])
                if user.password == data['password']:
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS,
                                         '登录成功', extra_tags='success')
                    return HttpResponseRedirect(request.session['login_from'])
                else:
                    messages.add_message(request, messages.ERROR,
                                         '密码错误', extra_tags='danger')
                    return render(request, 'accounts/login.html')
            except:
                messages.add_message(request, messages.ERROR,
                                     '用户不存在', extra_tags='danger')
        else:
            messages.add_message(request, messages.ERROR,
                                 '请检查填写的内容是否缺漏！', extra_tags='danger')
        return render(request, 'accounts/login.html')
    login_form = LoginForm()
    return render(request, 'accounts/login.html')


def user_register(request):
    if request.method == 'GET':
        request.session['register_from'] = request.META.get(
            'HTTP_REFERER', '/')
    if request.user.is_authenticated:
        messages.add_message(request, messages.SUCCESS,
                             '您已登录', extra_tags='success')
        return redirect("/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password']
            password2 = register_form.cleaned_data['password2']
            new_user = register_form.save(commit=False)
            # 设置密码
            if password1 != password2:  # 判断两次密码是否相同
                messages.add_message(request, messages.ERROR,
                                     '两次输入的密码不同！', extra_tags='danger')
                return render(request, 'accounts/register.html')
            else:
                same_username = User.objects.filter(username=username)
                if same_username:  # 用户名唯一
                    messages.add_message(request, messages.ERROR,
                                         '用户已经存在，请重新选择用户名！', extra_tags='danger')
                    return render(request, 'accounts/register.html')
            new_user.username = username
            new_user.password = password1
            new_user.save()
            # 保存好数据后立即登录并返回博客列表页面
            login(request, new_user)
            messages.add_message(request, messages.SUCCESS,
                                 '注册并登录成功', extra_tags='success')
            return HttpResponseRedirect(request.session['register_from'])
        else:
            messages.add_message(request, messages.ERROR,
                                 '用户已经存在，请重新选择用户名！', extra_tags='danger')
        return render(request, 'accounts/register.html')
    register_form = RegisterForm()
    return render(request, 'accounts/register.html')


def user_logout(request):
    # if request.method == 'GET':
    #     request.session['logout_to'] = request.META.get('HTTP_REFERER', '/')
    # if not request.session.get('is_login', None):
    #     # 如果本来就未登录，也就没有登出一说
    #     return HttpResponseRedirect(request.session['logout_to'])
    # # request.session.flush()
    logout(request)
    messages.add_message(request, messages.SUCCESS,
                         '登出成功', extra_tags='success')
    return redirect('/')


def profile_edit(request, id):
    if request.method == 'GET':
        request.session['edit_from'] = request.META.get(
            'HTTP_REFERER', '/')
    user = User.objects.get(id=id)
    # user_id 是 OneToOneField 自动生成的字段
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)
    if request.method == 'POST':
        if request.user != user:
            messages.add_message(request, messages.ERROR,
                                 '你没有权限修改！', extra_tags='danger')
            return render(request, 'accounts/edit.html')
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            # 取得清洗后的合法数据
            data = profile_form.cleaned_data
            if profile.phone != None:
                profile.phone = data['phone']
            if profile.email != None:
                profile.email = data['email']
            if profile.bio != None:
                profile.bio = data['bio']
            if 'img' in request.FILES:
                profile.img = data["img"]
            profile.save()
            # 带参数的 redirect()
            messages.add_message(request, messages.SUCCESS,
                                 '修改信息成功', extra_tags='success')
            return HttpResponseRedirect(request.session['edit_from'])
        else:
            messages.add_message(request, messages.ERROR,
                                 '输入信息不合法请重新输入！', extra_tags='danger')
            return render(request, 'accounts/edit.html')
    profile_form = ProfileForm()
    return render(request, 'accounts/edit.html')
