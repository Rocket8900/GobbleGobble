from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
# Need to pip install six (its to help fix compatibility issues betwen python 2 and 3)

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()
