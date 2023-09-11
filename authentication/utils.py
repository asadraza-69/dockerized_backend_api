from django.contrib.auth.models import User
import random


def generate_username(first_name, last_name = None):
    username = None
    loop_status = True
    i = 100
    fullname = first_name.replace(" ", "").lower()
    if last_name is not None:
        fullname += last_name.replace(" ", "").lower()
    while loop_status:
        username =  fullname + str(random.randint(1, i))
        obj = User.objects.filter(username=username)
        if not obj.exists():
            loop_status = False
        else:
            i += i
    return username

