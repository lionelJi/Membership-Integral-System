from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from accounts.forms import UserLoginForm, UserRegistForm, UserAddressForm
from accounts.models import User, UserAddress
from utils.verify import VerifyCode


def user_login(request):
    """ 用户登录 """
    # 如果登陆是从其他页面跳转过来的，会带一个next参数，
    # 如果有next参数，登陆完之后跳转到之前的地址去，否则到首页
    next_url = request.GET.get('next', 'index')
    # 第一次访问URL GET 展示表单，供用户输入
    # 第二次访问URL POST
    if request.method == 'POST':
        form = UserLoginForm(request=request, data=request.POST)
        print(request.POST)
        client = VerifyCode(request)
        code = request.POST.get('varify_code', None)
        rest = client.validate_code(code)
        print('验证结果: ', rest)
        # 表单是否通过了验证
        if form.is_valid():
            data = form.cleaned_data

            # user = User.objects.get(username=data['username'], password=data['password'])
            # request.session[constants.LOGIN_SESSION_ID] = user.id
            # return redirect('index')

            # 使用django-auth实现登陆
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                # 登陆
                login(request, user)
                # 登陆后的跳转
                return redirect(next_url)
        else:
            print(form.errors)
    else:
        form = UserLoginForm(request)
    return render(request, 'login.html', {
        'form': form,
        'next_url': next_url,
    })


def user_logout(request):
    """ 用户退出登陆 """
    logout(request)
    return redirect('index')


def user_register(request):
    """ 用户注册 """
    if request.method == 'POST':
        form = UserRegistForm(request=request, data=request.POST)
        if form.is_valid():
            # 调用注册方法
            form.register()
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = UserRegistForm(request=request)
    return render(request, 'register.html', {
        'form': form
    })


@login_required
def address_list(request):
    """ 地址列表 """
    my_addr_list = UserAddress.objects.filter(user=request.user, is_valid=True)
    return render(request, 'address_list.html', {
        'my_addr_list': my_addr_list
    })


@login_required()
def address_edit(request, pk):
    """ 地址新增或者是编辑 """
    user = request.user
    addr = None
    initial = {}
    # 如果pk是数字，则表示修改
    if pk.isdigit():
        # 查询相关的地址信息
        addr = get_object_or_404(UserAddress, pk=pk, user=user, is_valid=True)
        initial['region'] = addr.get_region_format()
    if request.method == 'POST':
        form = UserAddressForm(request=request,
                               data=request.POST,
                               instance=addr,
                               initial=initial)
        if form.is_valid():
            form.save()
            return redirect('accounts:address_list')
    else:
        form = UserAddressForm(request=request,
                               instance=addr,
                               initial=initial)
    return render(request, 'address_edit.html', {
        'form': form
    })


def address_delete(request, pk):
    """ 删除地址 """
    addr = get_object_or_404(UserAddress, pk=pk, user=request.user, is_valid=True)
    addr.is_valid = False
    addr.save()
    return HttpResponse('OK')
