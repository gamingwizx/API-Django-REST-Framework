from rest_framework.authentication import TokenAuthentication

class MyTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            # raise exceptions.AuthenticationFailed(_('Invalid token.'))
            return None

        if not token.user.is_active:
            # raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
            return None
        return token.user, token
    