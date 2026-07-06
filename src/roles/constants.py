from enum import Enum


class RoleEnum(str, Enum):
    """Single source of truth for role names.

    Roles live in the database (see src/roles/models.py), but the *names*
    that the code checks against must come from ONE place so that seeding
    and authorization never drift apart. Inheriting from `str` means the
    members compare directly against the `Role.name` column value.

        RoleEnum.ADMIN == "ADMIN"   # -> True
    """

    ADMIN = "ADMIN"
    USER = "USER"


# Descriptions used when seeding the roles table.
ROLE_DESCRIPTIONS: dict[RoleEnum, str] = {
    RoleEnum.ADMIN: "Administrator: manages movies, showtimes, auditoriums and users.",
    RoleEnum.USER: "Registered user: browses showtimes and reserves seats.",
}
