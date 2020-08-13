from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, NumberRange

class AddItemForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    image = FileField('Item Image', validators=[FileAllowed(['jpg', 'png'])])
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=10, max=100000)])
    submit = SubmitField('Add Item')

class UpdateItemForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    image = FileField('Item Image', validators=[FileAllowed(['jpg', 'png'])])
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=10, max=100000)])
    submit = SubmitField('Update Item')