"""
URL configuration for ventures project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from carsapp.views import home_view, login_assessor, dashboard, upload_excel
from carsapp.views import admin_uploaded_files, download_excel, convert_excel_to_pdf

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',home_view, name='home'),
    path('login/',login_assessor,name='login_assessor' ),
    path('dashboard/',dashboard, name='dashboard'),
    path('upload', upload_excel, name='upload_excel'),
    path('uploaded-files/', admin_uploaded_files, name='admin_uploaded_files'),
    path('download-excel/<int:file_id>/', download_excel, name='download_excel'),
    path('convert-excel-to-pdf/<int:file_id>/', convert_excel_to_pdf, name='convert_excel_to_pdf'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
