from collections import OrderedDict

from flask_wtf import FlaskForm
from wtforms import (
  SelectField,
  StringField,
  BooleanField,
  IntegerField,
)
from wtforms.validators import (
  DataRequired,
  Length,
  Optional,
  Regexp,
  NumberRange
)
from wtforms_alchemy.validators import Unique

from lib.util_wtforms import ModelForm, choices_from_dict
from app.blueprints.user.models import User


class SearchForm(FlaskForm):
    q = StringField('Search terms', [Optional(), Length(1, 256)])


class BulkDeleteForm(FlaskForm):
    SCOPE = OrderedDict([
        ('all_selected_items', 'All selected items'),
        ('all_search_results', 'All search results')
    ])

    scope = SelectField('Privileges', [DataRequired()],
                        choices=choices_from_dict(SCOPE, prepend_blank=False))


class UserForm(ModelForm):
    username_message = 'Letters, numbers and underscores only please.'

    coins = IntegerField('Coins', [DataRequired(),
                                   NumberRange(min=1, max=2147483647)])

    username = StringField(validators=[
        Unique(User.username),
        Optional(),
        Length(1, 16),
        Regexp(r'^\w+$', message=username_message)
    ])

    role = SelectField('Privileges', [DataRequired()],
                       choices=choices_from_dict(User.ROLE,
                                                 prepend_blank=False))
    active = BooleanField('Yes, allow this user to sign in')


    # def validate(self):
    #     if not FlaskForm.validate(self):
    #         return False
    #
    #     result = True
    #
    #     code = self.code.data.upper()
    #     percent_off = self.percent_off.data
    #     amount_off = self.amount_off.data
    #
    #     if Coupon.query.filter(Coupon.code == code).first():
    #         unique_error = 'Already exists.'
    #         self.code.errors.append(unique_error)
    #         result = False
    #     elif percent_off is None and amount_off is None:
    #         empty_error = 'Pick at least one.'
    #         self.percent_off.errors.append(empty_error)
    #         self.amount_off.errors.append(empty_error)
    #         result = False
    #     elif percent_off and amount_off:
    #         both_error = 'Cannot pick both.'
    #         self.percent_off.errors.append(both_error)
    #         self.amount_off.errors.append(both_error)
    #         result = False
    #     else:
    #         pass
    #
    #     return result
