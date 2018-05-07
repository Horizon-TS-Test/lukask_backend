from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """
    ALLOW USERS TO EDIT THEIR OWN PROFILE.
    """

    def has_object_permission(self, request, view, obj):
        """
        CHECK USER IS TRYING TO EDIT THEIR OWN PROFILE
        """

        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id


class UserProfilePublication(permissions.BasePermission):
    """
    ALLOW USERS TO UPDATE THEIR OWN TODOS
    """

    def has_permission(self, request, view):
        """
        RETURN TRUE IF USER REQUESTS FOR THEIR OWN TODOS, OTHERWISE RETURN FALSE
        """
        print ('Login_User: {}'.format(request.user))
        user_register = view.get_user_register(request.user.id)

        return user_register.id == request.user.id

    def has_object_permission(self, request, view, obj):
        """
        CHECKS THE USER IS TRYING TO UPDATE THEIR OWN TODOS.
        """
        print ('requestpinches: {}'.format(request))
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_register.id == request.user.id


class UserProfileTodo1(permissions.BasePermission):
    """
    ALLOW USERS TO UPDATE THEIR OWN TODOS
    """

    def has_permission(self, request, view):
        """
        RETURN TRUE IF USER REQUESTS FOR THEIR OWN TODOS, OTHERWISE RETURN FALSE
        """

        # IF THERE'S NOT A USER WITH REQUEST "kwargs" "user_id" THEN RETURN TRUE
        # REF: https://stackoverflow.com/questions/29660423/how-can-i-access-url-parameters-from-within-a-basepermission
        user_profile = view.get_user_profile(int(request.resolver_match.kwargs.get('user_id')))

        return user_profile.id == request.user.id

    def has_object_permission(self, request, view, obj):
        """
        CHECKS THE USER IS TRYING TO UPDATE THEIR OWN TODOS.
        """

        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_profile.id == request.user.id