from django import forms
from django.utils.encoding import force_text


class SpriteImageFormField(forms.TypedChoiceField):

    def valid_value(self, value):
        """Check to see if the provided value is a valid choice"""
        text_value = force_text(value)
        for k, v in self.choices:
            if value == k or text_value == force_text(k):
                return True
        return False
