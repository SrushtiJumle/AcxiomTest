from django import forms
from .models import Membership, Book

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['membership_number', 'first_name', 'last_name', 'contact_number', 'address', 'duration']
        widgets = {
            'duration': forms.RadioSelect,
        }

class UpdateMembershipForm(forms.ModelForm):
    extend_membership = forms.BooleanField(required=False, initial=True, label="Extend Membership (6 months)")
    cancel_membership = forms.BooleanField(required=False, label="Cancel Membership")

    class Meta:
        model = Membership
        fields = ['membership_number', 'first_name', 'last_name', 'contact_number', 'address', 'start_date', 'end_date', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'readonly': 'readonly'}),
            'end_date': forms.DateInput(attrs={'readonly': 'readonly'}),
            'status': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields read-only as per "populated" requirement, but allow editing if needed? 
        # "Membership Number is mandatory, based on which the rest of the fields are populated."
        # Usually this means they are displayed. I'll keep them editable for now or readonly if strictly just for viewing.
        # But "User can extend their membership or cancel their membership".
        # So maybe only buttons/checkboxes for action.
        
        self.fields['contact_number'].widget.attrs['readonly'] = True
        self.fields['address'].widget.attrs['readonly'] = True

class IssueBookForm(forms.Form):
    membership_number = forms.ModelChoiceField(queryset=Membership.objects.filter(status='Active'), to_field_name='membership_number', label='Member')
    book = forms.ModelChoiceField(queryset=Book.objects.filter(status='Available'), label='Book')

class ReturnBookForm(forms.Form):
    book_isbn = forms.CharField(label='Book ISBN')

class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn']


