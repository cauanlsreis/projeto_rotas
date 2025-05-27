from django.contrib import admin
from .models import Usuario
from django.contrib.auth.admin import UserAdmin

class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('id', 'email', 'nome', 'cpf', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'nome', 'cpf')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'senha', 'nome', 'cpf')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas importantes', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome', 'cpf', 'senha1', 'senha2', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(Usuario, UsuarioAdmin)
