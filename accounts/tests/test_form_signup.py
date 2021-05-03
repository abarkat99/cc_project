from django.test import TestCase

from ..forms import UserCreationForm


class SignUpFormTest(TestCase):
    def test_form_has_fields(self):
        form = UserCreationForm()
        expected = ['username', 'email', 'password1', 'password2']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
