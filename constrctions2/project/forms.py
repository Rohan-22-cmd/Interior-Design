# forms.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)



from django import forms
from .models import Consultation

class ConsultationForm(forms.ModelForm):
    email = forms.EmailField()
    platform_choice = forms.ChoiceField(
        choices=[
            ('google_meet', 'Google Meet'),
            ('zoom', 'Zoom'),
            ('whatsapp', 'WhatsApp'),
        ],
        required=True,
        label='Preferred Platform',
        widget=forms.RadioSelect  # Or you can use a Dropdown (Select) instead
    )
    class Meta:
        model = Consultation
        fields = ['name', 'email', 'phone']

    

