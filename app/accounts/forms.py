from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import User


class RegisterForm(forms.ModelForm):
    # Pido email, nombre completo y contraseña con confirmación para el registro

    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, label="Confirm password"
    )

    class Meta:
        model = User
        fields = ["email", "full_name"]

    def clean_full_name(self):
        # Reviso que el nombre completo tenga al menos 5 caracteres antes de guardar
        full_name = self.cleaned_data.get("full_name", "")
        if len(full_name.strip()) < 5:
            raise forms.ValidationError(
                "Full name must be at least 5 characters long."
            )
        return full_name.strip()

    def clean_password(self):
        # Dejo que Django valide la contraseña con las reglas definidas en settings
        password = self.cleaned_data.get("password")
        if password:
            from django.contrib.auth.password_validation import validate_password
            validate_password(password, self.instance)
        return password

    def clean(self):
        cleaned = super().clean()
        pw1 = cleaned.get("password")
        pw2 = cleaned.get("password_confirm")
        if pw1 and pw2 and pw1 != pw2:
            self.add_error("password_confirm", "Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    # Cambio el campo username por email para que el login use el correo

    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"autofocus": True}),
    )
