import re
import phonenumbers
from typing import Optional, Union, Type
from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_email_validator
from django.utils.translation import ugettext_lazy as _

class AuthValidator:
    @staticmethod
    def validate_email(email: Optional[str]) -> Optional[str]:
        if not email:
            raise ValidationError(_('Email field cannot be empty'))
        
        try:
            django_email_validator(email)

            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                raise ValidationError(_('Invalid email format'))
            
            return email.lower().strip()
        except ValidationError:
            raise ValidationError(_('Invalid email address'))
        
    @staticmethod
    def validate_phone_number(phone_number: Optional[str]) -> Optional[str]:
        if not phone_number:
            raise ValidationError(_('Phone number cannot be empty'))
        
        try:
            cleaned_number = re.sub(r'[^\d+]', '', phone_number)

            parsed_number = phonenumbers.parse(cleaned_number, None)

            if not phonenumbers.is_valid_number(parsed_number):
                raise ValidationError(_('Invalid phone number'))
            
            return phonenumbers.format_number(
                parsed_number,
                phonenumbers.PhoneNumberFormat.E164
            )
        except (phonenumbers.phonenumberutil.NumberParseException, ValidationError):
            raise ValidationError(_('Invalid phone number format'))
        
    @staticmethod
    def validate_password(password: str, min_length: int = 8) -> str:
        if not password:
            raise ValueError(_('Password cannot be empty'))
        
        if len(password) < min_length:
            raise ValueError(_(f'Password must at least contain {min_length} characters long'))
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError(_('Password must contain at least one uppercase letter'))
        
        if not re.search(r'[a-z]', password):
            raise ValidationError(_('Password must contain at least one lowercase letter'))

        if not re.search(r'\d', password):
            raise ValidationError(_('Password must contain at least one number'))
        
        if not re.search(r'[a-z]', password):
            raise ValidationError(_('Password must contain at least one lowercase letter'))
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(_('Password must contain at least one special character'))
        
        return password
    
    @staticmethod
    def valid_login_credentials(credential: str, user_model: Type[AbstractUser]) -> dict:
        try:
            validated_email = AuthValidator.validate_email(credential)

            try:
                user = user_model.objects.get(email=validated_email)
                return {
                    'type': 'email',
                    'value': validated_email,
                    'user': user
                }
            except user_model.DoesNotExist:
                raise ValidationError(_('No user found with this email'))
            
        except ValidationError:
            try:
                validated_phone = AuthValidator.validate_phone_number(credential)

                try:
                    user = user_model.object.get(phone_number=validated_phone)
                    return {
                        'type': 'phone',
                        'value': validated_phone,
                        'user': user
                    }
                except user_model.DoesNotExist:
                    raise ValidationError(_('No user found with this phone number'))
                
            except ValidationError:
                raise ValidationError(_('Invalid login credentials'))