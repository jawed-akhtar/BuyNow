from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from buynow.models import Warehouse

class AddWarehouseForm(FlaskForm):
    city = StringField('City', validators=[DataRequired()])
    submit = SubmitField('Add Warehouse')

    def validate_city(self, city):
        warehouse = Warehouse.query.filter_by(city=city.data).first()
        if warehouse:
            raise ValidationError('This warehouse is already added')

class UpdateWarehouseForm(FlaskForm):
    city = StringField('City', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_city(self, city):
        warehouse = Warehouse.query.filter_by(city=city.data).first()
        if warehouse:
            raise ValidationError('This warehouse is already added')