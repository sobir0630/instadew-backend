from django.contrib.auth.models import (
    BaseUserManager
)


class UserManager(BaseUserManager):
    """
        Foydalanuvchi yaratish va superfoydalanuvchi yaratish uchun maxsus manager.
    Args:
        BaseUserManager (_type_): Django tomonidan taqdim etilgan foydalanuvchi manageri, foydalanuvchi yaratish va autentifikatsiya jarayonlarini boshqarish uchun ishlatiladi.
    """
    def create_user(self, email, username, full_name, password=None, **extra_fields):
        """_summary_

        Args:
            email (_type_): email manzili, foydalanuvchining noyob identifikatori sifatida ishlatiladi.
            username (_type_): foydalanuvchining login uchun ishlatiladigan nomi, noyob bo'lishi kerak.
            password (_type_, optional): foydalanuvchining paroli. Defaults to None.
            cnf_password (_type_, optional): parolni tasdiqlash maydoni. Defaults to None.

        Raises:
            ValueError: Agar email kiritilmasa, bu xato yuz beradi.

        Returns:
            _type_: Yaratilgan foydalanuvchi obyekti.
        """
        if not email:
            raise ValueError("Foydalanuvchi yaratish uchun email manzili kiritilishi kerak.")
        
        if self.model.objects.filter(email=email).exists():
            raise ValueError("Bu email manzili bilan foydalanuvchi allaqachon mavjud.")

        if not username:
            raise ValueError("Foydalanuvchi yaratish uchun username kiritilishi kerak.")
        
        if not full_name:
            raise ValueError("Foydalanuvchi yaratish uchun full_name kiritilishi kerak.")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, full_name=full_name, **extra_fields)
        
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, full_name, password=None, **extra_fields):
        """_summary_

        Args:
            email (_type_): email manzili, superfoydalanuvchining noyob identifikatori sifatida ishlatiladi.
            username (_type_): superfoydalanuvchining login uchun ishlatiladigan nomi, noyob bo'lishi kerak.
            full_name (_type_): superfoydalanuvchining to'liq ismi.
            password (_type_, optional): superfoydalanuvchining paroli. Defaults to None.
            cnf_password (_type_, optional): superfoydalanuvchining parolni tasdiqlash maydoni. Defaults to None.

        Returns:
            CustomUser: Yaratilgan superfoydalanuvchi obyekti.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, username, full_name, password, **extra_fields)


         
