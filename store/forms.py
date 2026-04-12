from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from store.models import Product, Category, Make, Tag
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()

# --- AUTHENTICATION ---

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'email',
            Submit('submit', "Créer mon compte", css_class='btn btn-primary w-100 mt-3 shadow-sm')
        )

    class Meta:
        model = User
        fields = ['username', 'email']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur ou Email', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe', 'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', "Se connecter", css_class='btn btn-primary w-100 mt-3')
        )

# --- USER PROFILE ---

class EditUserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
            ),
            Submit('submit', "Mettre à jour le profil", css_class='btn btn-info w-100 mt-3 text-white')
        )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

# --- STORE MANAGEMENT ---

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'description',
            Row(
                Column('price', css_class='form-group col-md-6 mb-0'),
                Column('quantity', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('category', css_class='form-group col-md-4 mb-0'),
                Column('make', css_class='form-group col-md-4 mb-0'),
                Column('tags', css_class='form-group col-md-4 mb-0'),
            ),
            'slug',
            'image',
            Submit('submit', "Enregistrer le produit", css_class='btn btn-success w-100 mt-3')
        )

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity','category','slug','make','tags', 'image']

class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Ajouter la catégorie', css_class='btn btn-primary'))

    class Meta:
        model = Category
        fields = ['name']

class MakeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'is_partner',
            Submit('submit', 'Valider la marque', css_class='btn btn-primary')
        )

    class Meta:
        model = Make
        fields = ['name', 'is_partner']

class TagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Ajouter le Tag', css_class='btn btn-secondary'))

    class Meta:
        model = Tag
        fields = ['name']

class EditPasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Modifier le mot de passe', css_class='btn btn-warning w-100'))