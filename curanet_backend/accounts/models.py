"""
User model for the accounts app.
"""
from typing import Optional
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from core.constants.choices import UserRoles, AuthProviders
from core.utils.validators import AuthValidator

class UserManager(BaseUserManager):
    def create_user(self,
                    email: Optional[str]=None,
                    phone_number: Optional[str] = None,
                    password: Optional[str] = None,
                    **extra_fields
                    ) -> 'User':
        if not email and not phone_number:
            raise ValueError(_('Either email or phone number must be set.'))
        
        if email:
            email = AuthValidator.validate_email(self.normalize_email(email))
        if phone_number:
            phone_number = AuthValidator.validate_phone_number(phone_number)

        user = self.model(
            email=email,
            phone_number=phone_number,
            **extra_fields
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        
        user.save(using=self._db)
        return user
    
    def create_superuser(
        self,
        email: str,
        password: str,
        **extra_fields
    ) -> 'User':
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('role', UserRoles.ADMIN)

        if not email:
            # Can later set to an email with a specific domain
            raise ValueError(_('Superuser must have an email address'))
        
        return self.create_user(email=email, password=password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=True,
        blank=True,
        verbose_name=_('Email address')
    )
    phone_number = models.CharField(
        max_length=15, unique=True, 
        null=True, 
        blank=True,
        verbose_name=_('Phone number')
    )

    first_name = models.CharField(
        max_length=30,
        verbose_name=_('First name')
    )
    last_name = models.CharField(
        max_length=30,
        verbose_name=_('Last name')
    )

    role = models.CharField(
        max_length=20,
        choices=UserRoles.CHOICES,
        default=UserRoles.PATIENT,
        verbose_name=_('Role')
    )

    auth_provider = models.CharField(
        max_length=20,
        choices=AuthProviders.CHOICES,
        default=AuthProviders.EMAIL,
        verbose_name=_('Authentication provider')
    )

    license_number = models.CharField(
        max_length=50, 
        null=True, 
        blank=True,
        verbose_name=_('License number')
    )
    specialization = models.CharField(
        max_length=100, 
        null=True, 
        blank=True,
        verbose_name=_('Specialization')
    )

    address = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Address')
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date of birth')
    )

    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        null=True,
        blank=True,
        verbose_name=_('Profile picture')
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Active')
    )
    is_staff = models.BooleanField(
        default=True,
        verbose_name=_('Active')
    )
    is_verified = models.BooleanField(
        default=True,
        verbose_name=_('Verified')
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Date joined')
    )

    phone_verification_code = models.CharField(
        max_length=6, 
        null=True, 
        blank=True,
        verbose_name=_('Phone verification code')
    )
    phone_verification_expiry = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Phone verification expiry')
    )

    email_verification_code = models.CharField(
        max_length=6,
        null=True,
        blank=True,
        verbose_name=_('Email verification code')
    )
    email_verification_expiry = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Email verification expiry'))    

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']

    def __str__(self):
        return self.email or self.phone_number or str(self.id)
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def has_role_permission(self, permission: str) -> bool:
        return permission in UserRoles.ROLE_PERMISSIONS.get(self.role, [])