from rest_framework import permissions


class IsVendorPermissions(permissions.DjangoModelPermissions):
    # def has_permission(self, request, view):
    #     user = request.user
    #     if request.user.is_vendor():
    #         if user.has_perm('products.add_product'):
    #             return True
    #         if user.has_perm('products.change_product'):
    #             return True
    #         if user.has_perm('products.delete_product'):
    #             return True
    #         if user.has_perm('products.view_product'):
    #             return True
    #         return True
    #     return False

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


    def has_permission(self, request, view):
        user = request.user
        if not user.is_vendor:
            return False
        return super().has_permission(request, view)


    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)

