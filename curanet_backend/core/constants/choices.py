from enum import Enum
from typing import List, Dict, Any
from django.utils.translation import gettext_lazy as _


class UserRoles:
    """
    User role constants
    """
    ADMIN = 'admin'
    PHARMACIST = 'pharmacist'
    DOCTOR  = 'doctor'
    PATIENT = 'patient'

    CHOICES = [
        (ADMIN, _('Admin')),
        (PHARMACIST, _('Pharmacist')),
        (DOCTOR, _('Doctor')),
        (PATIENT, _('Patient'))
    ]

    ROLE_PERMISSIONS = {
        ADMIN: ['full_access'],
        PHARMACIST: ['view_inventory', 'manage_prescriptions'],
        DOCTOR: ['create_prescription', 'view_patient_records'],
        PATIENT: ['view_own_records']
    }

class AuthProviders:
    """
    Authentication provider constants
    """
    EMAIL = 'email'
    PHONE = 'phone'
    GOOGLE = 'google'
    FACEBOOK = 'facebook'

    CHOICES = {
        (EMAIL, _('Email')),
        (PHONE, _('Phone')),
        (GOOGLE, _('Google')),
        (FACEBOOK, _('Facebook'))
    }

class ValidationConstants:
    """
    Validation-related constants
    """
    
