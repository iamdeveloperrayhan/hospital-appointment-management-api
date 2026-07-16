from rest_framework.permissions import BasePermission, SAFE_METHODS

class AppointmentPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff:
            return True

        if user.user_type == "user":
            return obj.patient == user

        if user.user_type == "doctor":
            return obj.doctor.user == user


        return False

class BillPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated

        return (
            request.user.is_authenticated
            and request.user.is_staff
        )