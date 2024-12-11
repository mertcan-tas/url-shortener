from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, name, email, password, **extra_fields):
        if not name:
            raise ValueError("The name must be set")

        if not email:
            raise ValueError("The email must be set")
        
        email = self.normalize_email(email)
        user = self.model(
            name=name,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, name, password, **extra_fields):
        user = self.create_user(email=email, name=name, password=password, **extra_fields)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = False
        user.save()
        return user
    