from django import forms
from main.models import Person


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ['email', 'first_name',
                  'last_name', 'picture', 'fb_id']

    def clean(self):
        super().clean()
        email = self.cleaned_data.get('email')

        if not email:
            name = self.cleaned_data['first_name']
            email = '{}@anon.com'.format(name.lower())
            self.cleaned_data['email'] = email

        return self.cleaned_data

    def get_or_create_user(self):
        email = self.cleaned_data['email']
        try:
            return Person.objects.get(email=email)
        except Person.DoesNotExist:
            user = self.save(commit=False)
            user.username = email
            user.save()
            return user
