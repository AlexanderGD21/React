from rest_framework.throttling import SimpleRateThrottle


class _IpThrottle(SimpleRateThrottle):
    """Aplica límites por IP a flujos públicos sensibles."""

    def get_cache_key(self, request, view):
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request),
        }


class RegistrationThrottle(_IpThrottle):
    scope = 'registration'


class VerificationThrottle(_IpThrottle):
    scope = 'verification'


class PasswordRecoveryThrottle(_IpThrottle):
    scope = 'password_recovery'
