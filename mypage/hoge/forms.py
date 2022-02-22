from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from .models import Task


class AddTaskForm(forms.ModelForm):
    """タスク追加フォーム"""
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'set_date': AdminDateWidget(),  # インポートしたウィジェットを使う指示
        }
