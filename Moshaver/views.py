from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.dispatch import receiver


class CustomPasswordResetView:
    @receiver(reset_password_token_created)
    def password_reset_token_created(sender, reset_password_token, *args, **kwargs):
        """
          Handles password reset tokens
          When a token is created, an e-mail needs to be sent to the user
        """
        # send an e-mail to the user
        context ="لطفا برای بازیابی رمز خود به لینک زیر مراجعه کنید"+'\n'+"https://moshaver.markop.ir/{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

        send_mail(
            # title:
            "Password Reset for {}".format('Ostad Moshaver'),
            # message:
            context,
            # from:
            "ostadmoshaverteam@gmail.com",
            # to:
            [reset_password_token.user.email]
        )