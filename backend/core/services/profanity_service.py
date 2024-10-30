from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError

from better_profanity import profanity
from core.services.email_service import EmailService


class CheckProfanityService:

    @staticmethod
    def check_profanity(instance, description):
        if profanity.contains_profanity(description):
            current_attempts = instance.edit_attempts
            instance.edit_attempts = current_attempts + 1
            instance.is_active = False

            if current_attempts == 3:
                instance.save()
                EmailService.notify_admin(instance, description)
                raise ValidationError(_(f'You had only 3 attempts to change advertisement.'
                                        'Advertisement sent for review. '
                                        'Maximum edit attempts reached.'))

        else:
            instance.is_active = True if instance.edit_attempts < 3 else False

        instance.save()


