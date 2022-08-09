from rest_framework import permissions


class IsVendorPermissions(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        user = request.user
        if request.user.is_vendor():
            if user.has_perm('product.add_product'):
                return True
            if user.has_perm('product.change_product'):
                return True
            if user.has_perm('product.delete_product'):
                return True
            if user.has_perm('product.view_product'):
                return True
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)

