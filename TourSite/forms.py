from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    BaseUserCreationForm,
    AuthenticationForm,
)
from django.forms import DateField, ValidationError, ModelForm
from .models import Rate, Books

User = get_user_model()


class SignupForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
        )


    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email__iexact=email).exists():
            raise ValidationError("User with this email already exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.phone_number = self.cleaned_data["phone_number"]
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    ...


class AddRateForm(ModelForm):
    class Meta:
        model = Rate
        fields = {"tour", "stars", "comment"}

    def clear_rating(self):
        if not (0 <= self.cleaned_data.get("rai=ing") <= 5):
            raise ValidationError("Рейтинг має бути від 0 до 5")


class BookForm(ModelForm):
    class Meta:
        model = Books
        fields = {"tour", "comment"}