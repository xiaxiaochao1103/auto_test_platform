"""auto_test_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from auto_test import views
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r"^index/$",views.index),
    url(r"^module/$",views.module,name="module"),
    url(r"^moduletestcases/(?P<module_id>[0-9]+)/$",views.module_testcases,name="mtestcases"),
    url(r"^teststep/(?P<testcase_id>[0-9]+)$",views.teststep,name="caseteststep"),
    url(r"^testcase/$",views.testcase,name="testcase"),
    url(r"^testrecord/$",views.testrecord,name="testrecord"),
    url(r"^exceptioninfo/(?P<execute_id>[0-9]+)$",views.show_exception,name="showexception"),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    url(r'^teststeprecord/(?P<execute_id>[0-9]+)$', views.test_step_record,name="teststeprecord"),
    url(r'^pic/(?P<execute_id>[0-9]+)$', views.show_pic,name="showpic"),
    url(r"^exceptioninfo/(?P<execute_id>[0-9]+)$",views.show_exception,name="showexception"),
    url(r'^testsuit/',views.testsuit,name="testsuit"),
    url(r'^suitcases/(?P<suit_id>[0-9]+)$',views.show_testsuit_cases,name="suitcases"),
    url(r'^testsuitrecord/$',views.show_test_suit_record,name="showsuitrecord"),
    url(r'^testcaserecord/(?P<suit_record_id>[0-9]+)$',views.show_test_suit_test_case_record,name="showsuitcaserecord"),
    url(r"^suitexceptioninfo/(?P<test_case_record_id>[0-9]+)$",views.show_suit_exception,name="showsuitception"),
    url(r'^suitpic/(?P<test_case_record_id>[0-9]+)$', views.show_suit_pic,name="showsuitpic"),
    url(r'^suitteststeprecord/(?P<test_case_record_id>[0-9]+)$', views.test_suit_step_record,name="testsuitstepresult"),
    url(r'^managesuit/(?P<suit_id>[0-9]+)$',views.managesuit,name="managesuit"),
    url(r'^login/$', views.login),
    url(r'logout/$', views.logout),
]
