from django.utils.deprecation import MiddlewareMixin
from .utils import organization_manager


class AutoSelectOrganizationMiddleware(MiddlewareMixin):
  
  def process_request(self, request):
    if not hasattr(request, 'user'):
      return
    user = request.user

    if not user.is_authenticated:
      return

    orga = organization_manager.get_selected_organization(request)
    if orga is not None:
      return

    user_orgas = organization_manager.get_user_organizations(user)
    if user_orgas.count():
      orga = user_orgas.first()
      organization_manager.set_selected_organization(request, orga)
