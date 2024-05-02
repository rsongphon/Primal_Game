from PrimalGameAPI.models import RPiBoards , Primals , Games
from django import forms 
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML



class PrimalsForm(forms.Form):
    name = forms.CharField(max_length=255)
    
    

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username','first_name','last_name','email']
        
        
def validate_choice(value):
    if not(isinstance(value, int)):
        raise forms.ValidationError('Invalid choice selected')
    
class StartGameForm(forms.Form):
    def __init__(self, *args, **kwargs):
        rpi_name_list = RPiBoards.objects.all()
        primal_name_list = Primals.objects.all()
        game_name_list = Games.objects.all()
        
        rpi_choices = [(int(obj.pk), obj.board_name) for obj in rpi_name_list]
        primal_choices = [(int(obj.pk),  obj.name) for obj in primal_name_list]
        game_choices = [(int(obj.pk), obj.name) for obj in game_name_list]
        
        super(StartGameForm, self).__init__(*args, **kwargs)
        if rpi_name_list and primal_name_list and game_name_list:
            self.fields['rpi_name'] = forms.ChoiceField(choices=rpi_choices)
            self.fields['primal_name'] = forms.ChoiceField(choices=primal_choices)
            self.fields['game_name'] = forms.ChoiceField(choices=game_choices)
            
            
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<select name="my_field" class="form-control">'),
            *[(int(pk), str(choice)) for pk, choice in game_choices],
            *[(int(pk), str(choice)) for pk, choice in rpi_choices],
            *[(int(pk), str(choice)) for pk, choice in primal_choices],
            HTML('</select>'),
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )
    game_name = forms.ChoiceField(validators=[validate_choice])
    rpi_name = forms.ChoiceField( validators=[validate_choice])
    primal_name  = forms.ChoiceField(validators=[validate_choice])
    
    