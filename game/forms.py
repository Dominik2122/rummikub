from django import forms

from posts import models


class PostForm(forms.ModelForm):
    class Meta:
        fields = ("player")
        model = models.Game
