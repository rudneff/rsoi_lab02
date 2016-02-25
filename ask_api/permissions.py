from django.core.exceptions import ObjectDoesNotExist
from ask_api.models import Access
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        req_token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')
        if len(req_token) == 2 and req_token[0] in 'Bearer':
            access_token = req_token[1]
            try:
                access_obj = Access.objects.get(token=access_token)
                if not access_obj.is_expired():
                    request.user = access_obj.user
                    return True
            except ObjectDoesNotExist:
                pass
        return False


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        req_token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')
        if len(req_token) == 2 and req_token[0] in 'Bearer':
            access_token = req_token[1]
            try:
                access_obj = Access.objects.get(token=access_token)
                if not access_obj.is_expired() and obj.author_id == access_obj.user_id:
                    request.user = access_obj.user
                    return True
            except ObjectDoesNotExist:
                pass
        return False
