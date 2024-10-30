import os

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from core.services.jwt_service import ActivateToken, JWTService, RecoveryToken

UserModel = get_user_model()


class EmailService:

    @staticmethod
    def __send_email(to:str, template_name:str, context:dict, subject='') -> None:
        template = get_template(template_name)
        html_content = template.render(context)
        msg = EmailMultiAlternatives(subject=subject, from_email=os.environ.get('EMAIL_HOST_USER'), to=[to])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

    @classmethod
    def register(cls, user):
        token = JWTService.create_token(user, ActivateToken)
        url = f'http://localhost:3000/register/{token}'
        cls.__send_email(user.email,
                         'register.html',
                         {
                             'first_name':user.profile.first_name,
                             'url':url
                         },
                         'Register email')

    @classmethod
    def recovery(cls, user):
        token = JWTService.create_token(user, RecoveryToken)
        url = f'http://localhost:3000/recovery/{token}'
        cls.__send_email(user.email,
                         'recovery.html',
                         {
                             'first_name': user.profile.first_name,
                             'url':url
                         },
                         'Recovery email')

    @classmethod
    def notify_admin(cls, instance, description):
        admin_email = UserModel.objects.filter(is_active=True,
                                               is_staff=True, ).values_list('email', flat=True).first()

        if not admin_email:
            return

        cls.__send_email(admin_email,
                         'additional_email_check.html',
                         {
                             'advertisement_id': instance.id,
                             'seller': instance.seller.user.email,
                             'description': description,
                             'car_info': f'{instance.car.car_brand}, '
                                         f'{instance.car.car_model}, '
                                         f'{instance.car.vin_code}',
                         },
                         'Need check user\'s email')
