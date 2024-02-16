from dataclasses import asdict, dataclass

from django.contrib.auth import get_user_model

from .utils import generate_random_username

User = get_user_model()


@dataclass
class UserRegisterInput:

    email: str
    password: str
    first_name: str
    last_name: str
    phone_number: str = None
    username: str = ""


def create_user(user_input: UserRegisterInput) -> User:
    user_input.username = generate_random_username(
        user_input.first_name, user_input.last_name
    )

    user = User.objects.create(**asdict(user_input))
    if user_input.password is not None:
        user.set_password(user_input.password)
    else:
        user.set_unusable_password()

    user.full_clean()
    user.save()
    return user
