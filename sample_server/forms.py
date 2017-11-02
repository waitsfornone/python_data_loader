from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import (UUID, DataRequired)


class InstructionForm(FlaskForm):
    integration_id = StringField(
        'Integration ID',
        validators=[UUID(), DataRequired()])
    tenant_id = StringField('Tenant ID', validators=[UUID(), DataRequired()])
    active = BooleanField('Current Rule', default="true")
    run_next = BooleanField('Run Next Poll', default="")
    db_info = TextAreaField('DB Connection Info', validators=[DataRequired()])
    command = TextAreaField('DB Query', validators=[DataRequired()])
