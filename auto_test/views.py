from django.shortcuts import render, redirect
from . import models
from .forms import UserForm
import traceback
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import HttpResponse
import traceback
from django.contrib import auth  # 引入auth模块
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# from . import tasks
from . import utils

@login_required
def index(request):
    print("login success!",request.user.is_authenticated)
    projects = models.Project.objects.filter().order_by('id')
    print("projects:",projects)
    return render(request, 'auto_test/index.html', {'projects': get_paginator(request,projects) })


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    print("**********" * 10, )
                    auth.login(request, user)
                    return redirect('/index/')
                else:
                    message = "用户名不能存在或者密码不正确！"
            except:
                message = "登录程序出现错误"
                traceback.print_exc()
        return render(request, 'auto_test/login.html', locals())

    login_form = UserForm()
    return render(request, 'auto_test/login.html', locals())


def register(request):
    pass
    return render(request, 'auto_test/register.html')


@login_required
def logout(request):
    auth.logout(request)
    request.session.flush()
    return redirect("/login/")

def get_paginator(request, data):
    paginator = Paginator(data, 10)
    paginator_pages = ""

    # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
    page = request.GET.get('page')
    try:
        paginator_pages = paginator.page(page)
    # todo: 注意捕获异常
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        paginator_pages = paginator.page(1)
    except InvalidPage:
        # 如果请求的页数不存在, 重定向页面
        return HttpResponse('找不到页面的内容')
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        paginator_pages = paginator.page(paginator.num_pages)
    print("----------------", paginator_pages)
    print("----------------", paginator_pages.has_previous())
    print("----------------", paginator_pages.has_next())

    return paginator_pages


@login_required
def module(request):
    modules=""
    if request.method == "GET":
        modules = models.Module.objects.filter().order_by('id')
    else:
        proj_name = request.POST['proj']
        print("proj_name:",proj_name)
        projs =models.Project.objects.filter(name__contains=proj_name.strip()).order_by('id')
        projs = [proj.id for proj in projs]
        print("projs: ", projs)
        modules = models.Module.objects.filter(belong_project__in=projs).order_by('id')
        print("modules: %s" % modules)
    return render(request, 'auto_test/module.html', {'modules': get_paginator(request,modules) })


@login_required
def module_testcases(request,module_id):
    testcases=""
    module=""
    if module_id:#访问的时候，会从url中提取模块的id，根据模块id查询到模块数据，在模板中展现
        module = models.Module.objects.get(id=int(module_id))
    if request.method=="POST":#如果是post方法，收到所有的测试用例id，提交给测试用例执行表
        testcases_list = request.POST.getlist('testcases_list')
        if testcases_list:
            for testcase in testcases_list:
                test_case = models.TestCase.objects.get(id=int(testcase))
                #把选中的用例添加到测试用例执行表中，用celery去执行
                execute_record=models.TestCaseExecuteRecord.objects.create(test_case=test_case,status=0)
                task_id=utils.web_test_task(execute_record.id,test_case)
        else:
            print("运行测试用例失败")
            return HttpResponse("提交的运行测试用例为空，请选择用例后在提交！")
    testcases = models.TestCase.objects.filter(belong_module=module).order_by('id')
    return render(request, 'auto_test/testcase.html', {'testcases': get_paginator(request,testcases) })

@login_required
def testcase(request):
    testcases=""
    if request.method == "GET":
        testcases = models.TestCase.objects.filter().order_by('id')
    elif request.method=="POST":
        testcases_list = request.POST.getlist('testcases_list')
        if testcases_list:
            for testcase in testcases_list:
                test_case = models.TestCase.objects.filter(id=int(testcase))
                test_case_execute_record=models.TestCaseExecuteRecord.objects.create(test_case=test_case[0],status=0)
                task_id=utils.web_test_task(test_case_execute_record.id,test_case[0])
        else:
            print("运行测试用例失败")
            return HttpResponse("提交的运行测试用例为空，请选择用例后在提交！")
        testcases = models.TestCase.objects.filter().order_by('id')
    return render(request, 'auto_test/testcase.html', {'testcases': get_paginator(request,testcases) })

@login_required
def teststep(request,testcase_id):
    testcase_id=int(testcase_id)
    test_case =  models.TestCase.objects.get(id=testcase_id)
    #print("**********",test_case)
    teststeps = models.CaseStep.objects.filter(test_case = test_case).order_by('id')
    #print("**********",teststeps)
    return render(request, 'auto_test/teststep.html', {'teststeps': get_paginator(request,teststeps) })


@login_required
def testrecord(request):
    testrecords = models.TestCaseExecuteRecord.objects.filter().order_by('-id')
    return render(request, 'auto_test/testrecord.html', {'testrecords': get_paginator(request,testrecords) })

@login_required
def show_exception(request,execute_id):
    testrecord = models.TestCaseExecuteRecord.objects.get(id=execute_id)
    return render(request, 'auto_test/exceptioninfo.html', {'exception_info': testrecord.exception_info })

@login_required
def show_pic(request,execute_id):
    testrecord = models.TestCaseExecuteRecord.objects.get(id=execute_id)
    return render(request, 'auto_test/showpic.html', {'pic_path': testrecord.capture_screen })

@login_required
def test_step_record(request,execute_id):
    test_step_results = models.TestCaseStepExecuteRecord.objects.filter(test_case_execute_record =execute_id)
    return render(request, 'auto_test/teststeprecord.html', {'test_step_results': get_paginator(request,test_step_results) })

@login_required
def testsuit(request):
    if request.method == "POST":
        count_down_time = 0
        if request.POST['delay_time']:
            try:
                count_down_time = int(request.POST['delay_time'])
            except:
                print("输入的延迟时间是非数字！")
        else:
            print("没有输入延迟时间")
        print("request.POST: ", request.POST)
        testsuits = request.POST.getlist('testsuits_list')
        if testsuits:
            print("------********", testsuits)
            for testsuit in testsuits:
                test_suit = models.TestSuit.objects.get(id=int(testsuit))
                username = request.user.username
                test_suit_record = models.TestSuitExecuteRecord.objects.create(test_suit=test_suit,
                                                                               run_time_interval=count_down_time,
                                                                               creator=username)
                task_id = utils.web_suit_task(test_suit_record.id, int(testsuit))
                # web_suit_task
        else:
            print("运行测试集合用例失败")
            return HttpResponse("运行的测试集合为空，请选择测试集合后再运行！")
    testsuits = models.TestSuit.objects.filter()
    return render(request, 'auto_test/testsuit.html', {'testsuits': get_paginator(request, testsuits)})


@login_required
def show_testsuit_cases(request, suit_id):
    test_suit = models.TestSuit.objects.get(id=suit_id)
    testcases = models.TestSuitTestCases.objects.filter(test_suit=test_suit)
    if request.method == "POST":
        testcases_list = request.POST.getlist('testcases_list')
        if testcases_list:
            print("------********", testcases_list)
            for testcase in testcases_list:
                test_case = models.TestCase.objects.get(id=int(testcase))
                models.TestSuitTestCases.objects.filter(test_suit=test_suit, test_case=test_case).first().delete()
        else:
            print("删除测试集合的测试用例失败")
            return HttpResponse("删除的运行测试用例为空，请选择用例后再进行删除！")
    test_suit = models.TestSuit.objects.get(id=suit_id)
    testcases = models.TestSuitTestCases.objects.filter(test_suit=test_suit)
    return render(request, 'auto_test/suitcases.html',
                  {'testcases': get_paginator(request, testcases), 'test_suit': test_suit})


@login_required
def managesuit(request, suit_id):
    test_suit = models.TestSuit.objects.get(id=suit_id)
    if request.method == "GET":
        testcases = models.TestCase.objects.filter().order_by('-id')
        print("testcases:", testcases)
    elif request.method == "POST":
        testcases_list = request.POST.getlist('testcases_list')
        if testcases_list:
            print("------********", testcases_list)
            for testcase in testcases_list:
                test_case = models.TestCaseInfo.objects.get(id=int(testcase))
                suitcase = models.TestSuitTestCases.objects.create(test_suit=test_suit, test_case=test_case)
        else:
            print("添加测试用例失败")
            return HttpResponse("添加的运行测试用例为空，请选择用例后再添加！")
        testcases = models.TestCase.objects.filter().order_by('-id')
    return render(request, 'auto_test/managesuit.html',
                  {'testcases': get_paginator(request, testcases), 'test_suit': test_suit})


@login_required
def show_test_suit_record(request):
    test_suit_records = models.TestSuitExecuteRecord.objects.filter().order_by('-id')
    return render(request, 'auto_test/testsuitrecord.html',
                  {'test_suit_records': get_paginator(request, test_suit_records)})


@login_required
def show_test_suit_test_case_record(request, suit_record_id):
    test_suit_execute_record = models.TestSuitExecuteRecord.objects.get(id=suit_record_id)
    test_cases_records = models.TestSuitTestCaseExecuteRecord.objects.filter(test_suit_record=test_suit_execute_record)
    return render(request, 'auto_test/testsuittestcaserecord.html',
                  {'test_cases_records': get_paginator(request, test_cases_records)})


@login_required
def show_suit_exception(request, test_case_record_id):
    test_case_record = models.TestSuitTestCaseExecuteRecord.objects.get(id=test_case_record_id)
    return render(request, 'auto_test/exceptioninfo.html', {'exception_info': test_case_record.exception_info})


@login_required
def show_suit_pic(request, test_case_record_id):
    test_case_record = models.TestSuitTestCaseExecuteRecord.objects.get(id=test_case_record_id)
    return render(request, 'auto_test/showpic.html', {'pic_path': test_case_record.capture_screen})


@login_required
def test_suit_step_record(request, test_case_record_id):
    test_case_record = models.TestSuitTestCaseExecuteRecord.objects.get(id=test_case_record_id)
    test_steps_records = models.TestSuitTestStepExecuteRecord.objects.filter(test_case_record=test_case_record)
    return render(request, 'auto_test/testsuitsteprecord.html',
                  {'test_steps_records': get_paginator(request, test_steps_records)})
