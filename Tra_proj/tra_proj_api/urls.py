"""Tra_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from api import views
from api.views import uploadfileAPIView,scanfileAPIView,graphfileViewSet,getjsonfileAPIView,getresultAPIView,uploadfile2APIView,fileinfoViewSet


router = DefaultRouter()
router.register(r'files', views.uploadfileViewSet)
router.register(r'graphs', views.graphfileViewSet)
router.register(r'fileinfo', views.fileinfoViewSet)


urlpatterns = [

    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/uploadfile/', uploadfileAPIView.as_view()),
    path('api/scanfile/', scanfileAPIView.as_view()),
    path('api/getjsonfile/', getjsonfileAPIView.as_view()),
    path('api/getresult/', getresultAPIView.as_view()),
    path('api/uploadfilev2/', uploadfile2APIView.as_view()),

]


