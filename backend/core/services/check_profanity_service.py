from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError

from better_profanity import profanity
from core.services.email_service import EmailService


class CheckProfanityValidationService:

    @staticmethod
    def check_profanity(instance, description):
        if profanity.contains_profanity(description):
            instance.edit_attempts += 1

            if instance.edit_attempts == 3:
                instance.is_active = False
                instance.save()
                EmailService.notify_admin(instance, description)
                raise ValidationError(_('Maximum edit attempts reached.'))

            remaining = 3 - instance.edit_attempts
            EmailService.notify_admin(instance, description)
            raise ValidationError(_(f'Inappropriate content detected. '
                                    f'You have {remaining} attempts remaining.'))
