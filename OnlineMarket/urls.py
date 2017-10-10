"""Graduation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from Graduation import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.search),
    url(r'^select-item/$', views.select),
    # url(r'^Post-item/$', views.PostItem),
     url(r'^product/$', views.test1),
    # url(r'^test2/$', views.test),
    url(r'^my-products/$', views.myProduct),
    url(r'^products/user/(?P<userId>[0-9]+)$',views.productsDetalis ),
    url(r'^update/user/(?P<id>[0-9]+)$', views.update),
    url(r'^inbox/$', views.inbox),
    url(r'^filtering/$', views.filteringCamera),
    url(r'^devices/$', views.filteringele),
    url(r'^Accessories/$', views.filterinAccessories),
    url(r'^scholarship/$', views.filterinscholarship),
    url(r'^notfound/$', views.notfound),

    url(r'^Books/$', views.filterinbooks),


    url(r'^test3/$', views.RecommendtionData),



    # url('test2/', include('social.apps.django_app.urls', namespace='social12')),
    # url('test2/', include('django.contrib.auth.urls', namespace='auth12')),

    url('', include('social.apps.django_app.urls', namespace='social')),

    url('', include('django.contrib.auth.urls', namespace='auth'))

]
