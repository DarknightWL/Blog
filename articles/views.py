# coding:utf-8
import datetime
import json
from django.shortcuts import render, redirect, reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from articles.models import Article as art
from articles.models import Users
from paging_util import paging_helper
# Create your views here.


def is_login(func):
    def inner(arg):
        login_data = arg.session.get('login_data', None)
        if not login_data:
            return redirect('/login')
        return func(arg)
    return inner


def home(request, page=1):
    # 分页功能
    cur_page = paging_helper.try_int(page)  # 转换数据类型
    art_count = art.objects.all().count()  # 数据总数量
    paging_info = paging_helper.PagingInfo(cur_page, art_count)  # 产生分页所需参数

    post_list = art.objects.all()[paging_info.start: paging_info.end]  # 每页的数据
    paging_html = paging_helper.paging_html(cur_page, paging_info.all_page_count, '/')  # 分页链接html标签

    login_data = request.session.get('login_data', None)
    return render(request, "home.html", {'post_list': post_list, 'login_data': login_data, 'paging_html': paging_html})


def detail(request, id):
    try:
        post = art.objects.get(id=int(id))
    except art.DoesNotExist:
        raise Http404
    login_data = request.session.get('login_data', None)
    return render(request, "post.html", {"post": post, 'login_data': login_data})


def archives(request, page=1):
    # 分页功能
    cur_page = paging_helper.try_int(page)  # 转换数据类型
    art_count = art.objects.all().count()  # 数据总数量
    paging_info = paging_helper.PagingInfo(cur_page, art_count)  # 产生分页所需参数

    # post_list = art.objects.all()[paging_info.start: paging_info.end]  # 每页的数据
    paging_html = paging_helper.paging_html(cur_page, paging_info.all_page_count, '/archives/')  # 分页链接html标签
    try:
        # post_list = art.objects.all()
        post_list = art.objects.all()[paging_info.start: paging_info.end]  # 每页的数据
    except art.DoesNotExist:
        raise Http404
    login_data = request.session.get('login_data', None)
    return render(request, 'archives.html', {'post_list': post_list, 'login_data': login_data, 'error': False, 'paging_html': paging_html})


def about_me(request):
    login_data = request.session.get('login_data', None)
    return render(request, 'aboutme.html', {'login_data': login_data})


def search_tag(request, tag):
    try:
        post_list = art.objects.filter(category=tag)
    except art.DoesNotExist as err:
        raise Http404
    login_data = request.session.get('login_data', None)
    return render(request, 'tag.html', {'post_list': post_list, 'login_data': login_data})


def search_time(request, time):
    try:
        post_list = art.objects.filter(date_time=time)
    except art.DoesNotExist as err:
        raise Http404
    login_data = request.session.get('login_data', None)
    return render(request, 'time.html', {'post_list': post_list, 'login_data': login_data})


def blog_search(request):
    login_data = request.session.get('login_data', None)
    if 's' in request.GET:
        s = request.GET.get('s', None)
        if not s:
            return redirect('/')
        else:
            post_list = art.objects.filter(title__icontains=s)
            if len(post_list) == 0:
                return render(request, 'archives.html', {'post_list': post_list,
                                                         'error': True,
                                                         'login_data': login_data}
                              )
            else:
                return render(request, 'archives.html', {'post_list': post_list,
                                                         'error': False,
                                                         'login_data': login_data}
                              )
    return redirect('/')


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('loginname', None)
        password = request.POST.get('loginpwd', None)
        if not username and not password:
            error = '请输入用户名和密码'
        elif not username:
            error = '用户名不能为空'
        elif not password:
            error = '密码不能为空'
        else:
            is_exist = Users.objects.filter(user_name=username).count()
            if is_exist != 0:
                error = '此用户名已被占用'
            else:
                Users.objects.create(user_name=username, password=password)
                error = '注册成功'
        return render(request, 'signin.html', {'error': error})

    return render(request, 'signin.html')


def login(request):
    login_data = request.session.get('login_data', None)
    if login_data:
        return HttpResponseRedirect(reverse('personal_page', args=(login_data['login_name'],)))
    if request.method == 'POST':
        login_name = request.POST.get('loginname')
        login_pwd = request.POST.get('loginpwd')
        try:
            req = Users.objects.get(user_name=login_name, password=login_pwd)
        except Users.DoesNotExist as error:
            error = '用户名或密码不正确，请重新输入。'
            return render(request, 'login.html', {"error": error})
        request.session['login_data'] = {'login_name': login_name}
        return HttpResponseRedirect(reverse('personal_page', args=(login_name,)))
    return render(request, 'login.html')


def logout(request):
    del request.session['login_data']
    return redirect('/')


@is_login
def write_blog(request):
    login_data = request.session.get('login_data', None)
    if request.method == 'POST':
        art_title = request.POST.get('title')
        art_category = request.POST.get('category')
        art_content = request.POST.get('article')
        art_author = login_data.get('login_name')
        try:
            if not art_title or not art_category:
                raise Exception("请检查博文题目和标签是否填写完整。")
            author_obj = Users.objects.get(user_name=art_author)
            art.objects.create(title=art_title, category=art_category, content=art_content, author=author_obj)
        except Exception as error:
            return render(request, 'error.html', {'login_data': login_data, 'write_error': error})
        return HttpResponseRedirect(reverse('personal_page', args=(art_author,)))
    return render(request, 'write.html', {'login_data': login_data})


def personal_page(request, username):
    login_data = request.session.get('login_data', None)
    if not login_data:
        return redirect('/login')
    post_list = art.objects.filter(author__user_name=login_data['login_name'])
    if len(post_list) == 0:
        return render(request, 'archives.html', {'post_list': post_list, 'error': True, 'login_data': login_data})
    else:
        return render(request, 'archives.html', {'post_list': post_list, 'error': False, 'login_data': login_data})


def delete_article(request):
    login_data = request.session.get('login_data', None)
    if not login_data:
        return render(request, 'login.html')
    if request.method == 'POST':
        art_id = request.POST.get('art_id')
        try:
            art_obj = art.objects.get(id=art_id)
            if login_data['login_name'] != art_obj.author.user_name:
                raise Exception('您无权限删除这篇博文')
            art_obj.delete()
        except Exception as error:
            return render(request, 'error.html', {'login_data': login_data, 'update_error': error})
        return HttpResponseRedirect(reverse('personal_page', args=(login_data['login_name'],)))


def update_article(request):
    login_data = request.session.get('login_data', None)
    if not login_data:
        return redirect('/login/')
    if request.method == 'GET':
        art_id = request.GET.get('art_id')
        try:
            art_obj = art.objects.get(id=art_id)
            if login_data['login_name'] != art_obj.author.user_name:
                raise Exception("您无权限修改这篇博文。")
            post_dict = {'art_title': art_obj.title,
                         'art_category': art_obj.category,
                         'art_content': art_obj.content}
            post_dict.setdefault('login_data', login_data)
        except Exception as error:
            return render(request, 'error.html', {'login_data': login_data, 'update_error': error})
        print(post_dict)
        return render(request, 'update.html', post_dict)
    elif request.method == 'POST':
        art_title = request.POST.get('title', None)
        art_category = request.POST.get('category', None)
        art_content = request.POST.get('article', None)
        art_id = int(request.META['HTTP_REFERER'].split('/')[-2])
        try:
            if not art_title or not art_category:
                raise Exception('请检查博文是否填写了题目和标签。')
            art_obj = art.objects.get(id=art_id)
            art_obj.title = art_title
            art_obj.category = art_category
            art_obj.content = art_content
            art_obj.save()
        except Exception as error:
            return render(request, 'error.html', {'login_data': login_data, 'update_error': error})
        return HttpResponseRedirect(reverse('personal_page', args=(login_data['login_name'],)))
