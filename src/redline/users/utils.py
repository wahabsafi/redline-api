from random import randint

from django.contrib.auth import get_user_model

User = get_user_model()


def generate_random_username(first_name: str, last_name: str, base=True) -> str:
    """generating username based on user first name and last name for users who dont provide username when they sign up"""
    username = (first_name + "_" + last_name).lower()
    if not base:
        username += str(randint(1, 10000))

    if not is_uniqe_username(username):
        return generate_random_username(first_name, last_name, base=False)
    return username


def is_uniqe_username(username: str) -> bool:
    return not User.objects.filter(username=username).exists()
