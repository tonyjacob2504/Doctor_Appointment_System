"""flutter_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from .import views
urlpatterns = [
    path('login/',views.all_login),
    path('admin/',views.admin_dash),
    path('dash/',views.admin_dash),
    path('doctors/',views.admin_doctor),
    path('users/',views.admin_users),
    path('complaint/',views.admin_complaint),
    path('reply/<int:rid>/',views.comp_reply),
    path('feedback/',views.admin_feedback),
    path('report/',views.reports),
    path('dregister/',views.doctor_register),
    path('accept/<int:rid>/',views.accept),
    path('reject/<int:rid>/',views.reject),
    path('uregister/',views.users_reg),
    path('ulogin/',views.users_login),
    path('appt/',views. book_appointment),
    path('apt_view/',views.appointment_view),
    path('add_rating/',views.add_rating),
    path('view_rating/<int:rid>/',views.view_rating),
    path('add_complaint/', views.add_complaint),
    path('view_complaints/', views.view_complaints),
    path('add_feedback/', views.add_feedback),

    
    path('user_accept/<int:rid>/',views.user_accept),
    path('user_reject/<int:rid>/',views.user_reject),
    path('dr_login/',views.dr_login),
    path('dr_dash/',views.dr_dash),
    path('dr_schedule/',views.dr_schedules),
    path('dr_fees/',views.dr_fees),
   
    path('fview_doctors/',views.view_doctors),
    path('vschedule/<int:rid>/',views.vschedule),
    path('dr_appointments/', views.doctor_appointments),
    path('appointment_status/<int:rid>/<str:status>/',views.appointment_status),
    path('dr_ratings/', views.doctor_ratings),
    path('dr_dash_view/', views.dash_view),


    path('view_schedule/', views.view_schedule),
    path('edit_schedule/<int:rid>/', views.edit_schedule),
    path('delete_schedule/<int:rid>/', views.delete_schedule),
    path('cancel_appointment/', views.cancel_appointment),
    path('update_appointment/', views.update_appointment, name='update_appointment'),


    path('logout/', views.user_logout),

    

    
        
    


    


    
]
