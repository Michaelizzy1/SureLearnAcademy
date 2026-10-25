from django import forms

from .models import ContactSubmission


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ["name", "phone", "course_interest", "level", "preferred_mode", "preferred_time", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "phone": forms.TextInput(attrs={"placeholder": "e.g. 0803 000 0000"}),
            "level": forms.TextInput(attrs={"placeholder": "e.g. SS2, beginner"}),
            "preferred_time": forms.TextInput(attrs={"placeholder": "e.g. Weekday evenings, Saturdays"}),
            "message": forms.Textarea(attrs={"rows": 3, "placeholder": "Goals, exam date, current struggles..."}),
        }
