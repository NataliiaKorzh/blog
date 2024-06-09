from django.contrib.auth import get_user_model


def get_subscribers():
    """
    Returns a list of all subscribers

    """
    return [user.id for user in get_user_model().objects.filter(is_subscribed=True)]
