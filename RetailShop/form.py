from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField, HiddenField
from wtforms.validators import Email, DataRequired, Length

class LoginForm(Form):
    username = StringField('Username', validators=[Length(min=1)],
                           render_kw={'autofocus': True, 'placeholder': 'Username'})
    password = PasswordField('Password', validators=[Length(min=3)],
                             render_kw={'placeholder': 'Password'})

class RegisterForm(Form):
    name = StringField('Name', validators=[Length(min=3, max=50)],
                       render_kw={'autofocus': True, 'placeholder': 'Full Name'})
    username = StringField('Username', validators=[Length(min=3, max=25)],
                           render_kw={'placeholder': 'Username'})
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=4, max=25)],
                        render_kw={'placeholder': 'Email'})
    password = PasswordField('Password', validators=[Length(min=3)],
                             render_kw={'placeholder': 'Password'})
    mobile = StringField('Mobile', validators=[Length(min=11, max=15)],
                         render_kw={'placeholder': 'Mobile'})


class MessageForm(Form):
    body = StringField('', validators=[Length(min=1)],
                       render_kw={'autofocus': True})

class OrderForm(Form):
    name = StringField('Full Name', validators=[Length(min=1), DataRequired()],
                       render_kw={'autofocus': True, 'placeholder': 'Full Name'})
    mobile_num = StringField('Mobile', validators=[Length(min=1), DataRequired()],
                             render_kw={'autofocus': True, 'placeholder': 'Mobile'})
    quantity = SelectField('Quantité', validators=[DataRequired()],
                           choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    order_place = StringField('Commandes', validators=[Length(min=1), DataRequired()],
                              render_kw={'placeholder': 'Order Place'})

class UpdateRegisterForm(Form):
    name = StringField('Full Name', validators=[Length(min=3, max=50)],
                       render_kw={'autofocus': True, 'placeholder': 'Full Name'})
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=4, max=25)],
                        render_kw={'placeholder': 'Email'})
    password = PasswordField('Password', validators=[Length(min=3)],
                             render_kw={'placeholder': 'Password'})
    mobile = StringField('Mobile', validators=[Length(min=11, max=15)],
                         render_kw={'placeholder': 'Mobile'})

class DeveloperForm(Form):
    id = StringField('Identifiant Produit', validators=[Length(min=1)],
                     render_kw={'placeholder': "Entrez l'identifiant d'un produit..."})

class AddToCartForm(Form):
    product_id = HiddenField('Product ID', validators=[DataRequired()])
    quantity = SelectField('Quantité', validators=[DataRequired()],
                          choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])

class CheckoutForm(Form):
    name = StringField('Nom complet', validators=[Length(min=1), DataRequired()],
                      render_kw={'autofocus': True, 'placeholder': 'Nom complet'})
    mobile = StringField('Téléphone', validators=[Length(min=1), DataRequired()],
                        render_kw={'placeholder': 'Numéro de téléphone'})
    address = StringField('Adresse de livraison', validators=[Length(min=1), DataRequired()],
                         render_kw={'placeholder': 'Adresse de livraison'})
