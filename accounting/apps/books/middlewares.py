from .utils import organization_manager


class AutoSelectOrganizationMiddleware:
  
  def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        
  def process_request(self, request):
    if not request.user or not request.user.is_authenticated:
      return

    orga = organization_manager.get_selected_organization(request)
    if orga is not None:
      return

    user_orgas = organization_manager.get_user_organizations(request.user)
    if user_orgas.count():
      orga = user_orgas.first()
      organization_manager.set_selected_organization(request, orga)

  def __call__(self, request):
    self.process_request(request)
    response = self.get_response(request)
    return response

