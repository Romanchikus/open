from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from allauth.account.forms import SignupForm
from . import models


User = get_user_model()


class ProfileCreateForm(SignupForm):
    USER_TYPES = [("student", "student"), ("professor", "professor")]
    user_type = forms.ChoiceField(choices=USER_TYPES)

    class Meta(auth_forms.UserCreationForm.Meta):
        model = User

    def save(self, request):
        user = super().save(request)

        user_type = self.cleaned_data["user_type"]
        user_type_class_map = {
            "professor": models.Professor,
            "student": models.Student,
        }
        user_class = user_type_class_map[user_type]
        profile = user_class()
        setattr(user, user_type, profile)
        user.save()
        profile.save()

        group = Group.objects.get(name=f"{user_type}s")
        group.user_set.add(user)
        group.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
        ]


class ProfessorForm(forms.ModelForm):
    class Meta:
        model = models.Professor
        fields = [
            "tel",
            "dob",
            "city",
            "bio",
            "edulevel",
            "yearsexperience",
            "picture",
        ]
        labels = {
            "tel": _("Telephone"),
            "dob": _("Data of birth"),
            "city": _("City"),
            "bio": _("Biography"),
            "edulevel": _("Education level"),
            "yearsexperience": _("Years of experience"),
            "picture": _("Picture"),
        }
        widgets = {"dob": forms.DateInput(attrs={"type": "date"})}


class StudentForm(forms.ModelForm):
    class Meta:
        model = models.Professor
        fields = [
            "dob",
            "city",
            "picture",
        ]
        labels = {
            "dob": _("Data of birth"),
            "city": _("City"),
            "picture": _("Picture"),
        }
        widgets = {"dob": forms.DateInput(attrs={"type": "date"})}


ProfessorFormSet = inlineformset_factory(
    User, models.Professor, form=ProfessorForm, exclude=[], extra=1, can_delete=False,
)

StudentFormSet = inlineformset_factory(
    User, models.Student, form=StudentForm, exclude=[], extra=1, can_delete=False,
)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ["score", "text"]
        labels = {
            "score": _("Score"),
            "text": _("Text"),
        }
