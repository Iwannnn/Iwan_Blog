from django import forms
from .models import Comment
from django.shortcuts import render, redirect


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
