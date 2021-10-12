from rest_framework import permissions 

class NoPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True


# class isUser(permissions.BasePermission):
#     message = "Action is not allowed"

#     def has_permission(self, request, view):
#         if request.user and request.user.groups.filter(name='investor'):
#             return True
#         return False

class isBank(permissions.BasePermission):
    message = "Action is not allowed"

    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='bank'):
            return True
        return False


class isCustomer(permissions.BasePermission):
    message = "Action is not allowed"

    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='customer'):
            return True
        return False        

class isInvestor(permissions.BasePermission):
    message = "Action is not allowed"

    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='investor'):
            return True
        return False

    # def has_object_permission(self, request, view,obj):
    #     return True
    #     return request.user.groups == obj.allowed
        