from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    """_summary_
    Customised User Manager for my Users
    """
    def email_validator(self, email):
        """_summary_

        Args:
            email (str): email Address
        """
        try:
            validate_email(email)
        except ValidationError:
            raise _("Email Address not Valid")

    def create_user(self, email, username, fullname, password, **extra_fields):
        """_summary_

        Args:
            email (email): Email Address
            username (str): Unique Username
            fullname (str): first and last name
            password (hash): password

        Raises:
            ValueError: ''
            ValueError: ''
            ValueError: ''
            ValueError: ''

        Returns:
            self.model: an instance of the User Manager
        """

        if not self.email:
            raise ValueError(_("Email must be provided"))
        if not self.username:
            raise ValueError(_("Username must not be blank"))
        if not self.fullname:
            raise ValueError(_("Full Name must not be blank"))

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("A valid Email Address must be provided for this account"))

        user = self.model(email=email, username=username, fullname=fullname, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, fullname, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("An Admin staff status must be True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("An Admin 'superuser' status must be True")

    # Returns an the createuser function
        return self.create_user(email, username, fullname, password, **extra_fields)