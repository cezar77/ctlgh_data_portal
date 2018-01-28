from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Reset


class AnimalFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AnimalFilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.form_action = '.'
        self.helper.add_input(Submit('submit', 'Search', css_class='btn btn-primary'))
        self.helper.add_input(Reset('reset', 'Clear', css_class='btn btn-warning'))
