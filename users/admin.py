from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    # Faqat o'qish mumkin bo'lgan maydonlar
    readonly_fields = ("created_at", "last_login")

    # Admin paneldagi jadvalda ko'rsatiladigan ustunlar
    list_display = (
        "id",
        "email",
        "username",
        "full_name",
        "is_staff",
        "is_active",
        "is_superuser",
        "created_at",
        "last_login",
    )

    # Jadvalda to'g'ridan-to'g'ri tahrirlash mumkin bo'lgan ustunlar
    list_editable = ("is_staff", "is_active")

    # Qidirish mumkin bo'lgan maydonlar
    search_fields = ("email", "username", "full_name")

    # Filtrlash mumkin bo'lgan maydonlar
    list_filter = ("is_staff", "is_active", "is_superuser", "groups")

    # Tartiblash (default ID bo'yicha)
    ordering = ("id",)

    # Formadagi maydonlarni guruhlash va chiroyli qilish
    fieldsets = (
        ("Asosiy ma'lumotlar", {"fields": ("email", "username", "full_name")}),
        ("Parol va ruxsatlar", {
            "fields": (
                "password",
                "is_staff",
                "is_active",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Muhim sanalar", {"fields": ("created_at", "last_login")}),
    )

    # Passwordni faqat ko‘rsatish (edit qilolmaydi)
    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields)
        if obj:  # mavjud foydalanuvchi tahrir qilinganida
            readonly.append("password")
        return readonly