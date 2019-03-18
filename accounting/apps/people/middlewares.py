from django.utils.deprecation import MiddlewareMixin

from django.shortcuts import redirect

from django.urls import reverse


class EnsureFiscalProfileMiddleware(MiddlewareMixin):
  
  def process_request(self, request):
    if not hasattr(request, 'user'):
      return
    user = request.user
    
    if not user.is_authenticated:
      return

    if not hasattr(user, 'fiscal_profile'):
      requested_path = request.path
      target_path = reverse('people:fiscalprofile-create')
      if requested_path == target_path:
        return 
      return redirect(to=target_path)
