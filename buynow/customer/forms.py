from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from buynow.models import Customer

class UpdateAccountForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    city = StringField('City', validators = [DataRequired(), Length(min=2, max=25)])
    profile_pic = FileField('Update Profile Pic', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save')

    def validate_email(self, email):   
        if current_user.email != email.data:
            customer = Customer.query.filter_by(email=email.data).first()
            if customer:
                raise ValidationError('Email is already been taken, Please choose another one')