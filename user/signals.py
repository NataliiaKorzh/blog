from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created, post_password_reset


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):

    """
    Signal handler for password reset token creation.

    This function is called when a password reset token is created. It sends an email to the user
    containing a link to reset their password.
    """

    user = reset_password_token.user
    reset_password_url = "{}?token={}".format(
        instance.request.build_absolute_uri(
            reverse("user:password_reset_confirm")
        ),
        reset_password_token.key,
    )

    email_plaintext_message = f"""
    Hello {user.username},

    You have requested a password reset for your account.
    Please click the link below to reset your password:

    {reset_password_url}

    If you did not request this, please ignore this email.

    Thank you,
    Some Website Title
    """

    email_html_message = f"""
    <html>
        <body>
            <p>Hello {user.username},</p>
            <p>You have requested a password reset for your account.</p>
            <p>Please click the link below to reset your password:</p>
            <p><a href="{reset_password_url}">Reset Password</a></p>
            <p>If you did not request this, please ignore this email.</p>
            <p>Thank you,<br>Some Website Title</p>
        </body>
    </html>
    """

    msg = EmailMultiAlternatives(
        subject="Password Reset for Some Website Title",
        body=email_plaintext_message,
        from_email="noreply@somehost.local",
        to=[user.email],
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()


@receiver(post_password_reset)
def delete_password_reset_token(sender, instance, *args, **kwargs):
    """
    Signal handler to delete password reset token after successful password reset.
    """
    reset_password_token = instance
    reset_password_token.delete()
