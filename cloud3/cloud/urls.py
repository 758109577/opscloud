"""cloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from ops import  views as ops_views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', ops_views.login),
    url(r'^user/', ops_views.user_manager),
    url(r'user_update/', ops_views.user_update),
    url(r'^user_delete/', ops_views.user_delete),
    url(r'index/', ops_views.index),
    url(r'form/', ops_views.form),
    url(r'^compiler/', ops_views.compiler_host),
    url(r'^update/', ops_views.compiler_update),
    url(r'^delete/', ops_views.compiler_delete),
    url(r'^node/', ops_views.node),
    url(r'node_update/', ops_views.node_update),
    url(r'node_delete/', ops_views.node_delete),
    url(r'^server/', ops_views.server),
    url(r'^server_app/', ops_views.server_app),
    url(r'^server_add/', ops_views.server_add),
    url(r'^server_del/', ops_views.server_del),
    url(r'^git_url/', ops_views.comp_mvn),
]
