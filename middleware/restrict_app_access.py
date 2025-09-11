from django.shortcuts import redirect
from django.urls import reverse

class AppAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        
        if user.is_superuser:
         return self.get_response(request)  # allow everything



        # Check if the user is logged in and has a user profile
        if user.is_authenticated and hasattr(user, 'userprofile'):
            allowed_app = user.userprofile.allowed_app.lower()
            path = request.path.lower()

            # Exceptions (home, logout, admin)
            if path == '/' or path.startswith('/admin/') or path == reverse('account:logout'):
                return self.get_response(request)

            # If allowed app in path, allow it
            if f"/{allowed_app}/" in path:
                return self.get_response(request)
            else:
                return redirect(f'/{allowed_app}/')  # Redirect to their allowed app

        return self.get_response(request)
