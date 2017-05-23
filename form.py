from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.fields.html5 import EmailField
from wtforms import validators
from model import Users

class RegistrationForm(Form):
    username = StringField('usuario',
    	[
    	validators.Required(message = 'Se requiere usuario'),
    	validators.length(min=4,max=25,message='Ingresa un usuario valido')
    	]
    	)
    password = PasswordField('password',
    	[
    	validators.Required(message = 'Se requiere usuario')
    	]
    	)
    email = EmailField('correo electronico',
    	[
    	validators.Required(message = 'Se requiere email'),
    	validators.Email(message='Ingresa un email valido'),
    	#validators.length(min=4,max=25,message='Ingresa un usuario valido')
    	]
    	)

    def validate_username(form,field):
        username = field.data
        user = Users.query.filter_by(username = username).first()
        if user is not None:
            raise validators.ValidationError('usuario ya utilizado')
    