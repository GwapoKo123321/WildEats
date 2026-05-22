ROLE_STUDENT = "student"
ROLE_VENDOR = "vendor"
ROLE_ADMIN = "admin"
ROLE_NAMES = {ROLE_STUDENT, ROLE_VENDOR, ROLE_ADMIN}


def user_role(user):
    if not user.is_authenticated:
        return ""
    if user.groups.filter(name=ROLE_ADMIN).exists():
        return ROLE_ADMIN
    if user.groups.filter(name=ROLE_STUDENT).exists():
        return ROLE_STUDENT
    if user.groups.filter(name=ROLE_VENDOR).exists():
        return ROLE_VENDOR
    if user.is_superuser:
        return ROLE_ADMIN
    if user.is_staff:
        return ROLE_VENDOR
    return ROLE_STUDENT


def is_admin(user):
    return user_role(user) == ROLE_ADMIN


def is_vendor(user):
    return user_role(user) == ROLE_VENDOR


def is_student(user):
    return user_role(user) == ROLE_STUDENT
