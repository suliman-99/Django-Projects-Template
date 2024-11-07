from enums.enums import AppType


def detect_user_role_by_app_type_header(request):
    user = request.user
    if not user.is_authenticated:
        return
    
    need_save = False

    if request.app_type == AppType.CUSTOMER and not user.is_customer:
        user.is_customer = True
        need_save = True

    if request.app_type == AppType.PROVIDER and not user.is_provider:
        user.is_provider = True
        need_save = True
        
    if need_save:
        user.save()


class UserRoleDetectorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith('/api/'):
            detect_user_role_by_app_type_header(request)
        return response
