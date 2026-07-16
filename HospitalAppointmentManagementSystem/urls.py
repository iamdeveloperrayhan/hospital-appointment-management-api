"""
URL configuration for HospitalAppointmentManagementSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from Accounts.views import (
    RegisterAPIView,
    ProfileAPIView,
    ForgotPasswordAPIView,
    ResetPasswordAPIView,
)
from DoctorManagement.views import (
        DoctorListCreateAPIView,
        DoctorDetailUpdateAPIView,
)
from AppointmentManagement.views import (
    AppointmentListCreateAPIView,
    AppointmentDetailAPIView
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from BillManagement.views import BillViewSet
from Dashboard.views import DashboardAPIView
from django.urls import include

router = DefaultRouter()
router.register("bills", BillViewSet, basename="bill")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/register/", RegisterAPIView.as_view()),
    path("api/login/", TokenObtainPairView.as_view()),
    path("api/refresh/", TokenRefreshView.as_view()),
    path("api/profile/", ProfileAPIView.as_view()),
    path("api/dashboard/", DashboardAPIView.as_view()),
    path("api/forgot-password/", ForgotPasswordAPIView.as_view()),
    path("api/reset-password/", ResetPasswordAPIView.as_view()),
    path("api/doctors/", DoctorListCreateAPIView.as_view()),
    path("api/doctors/<int:pk>/", DoctorDetailUpdateAPIView.as_view()),
    path("api/appointments/", AppointmentListCreateAPIView.as_view()),
    path("api/appointments/<int:pk>/", AppointmentDetailAPIView.as_view()),
    path("api/", include(router.urls)),
]
