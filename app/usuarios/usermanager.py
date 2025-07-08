from django.contrib.auth.base_user import BaseUserManager

class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, cpf, nome, senha=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        if not cpf:
            raise ValueError('O CPF é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, cpf=cpf, nome=nome, **extra_fields)
        user.set_password(senha)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, cpf, nome, senha=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, cpf, nome, senha, **extra_fields)
