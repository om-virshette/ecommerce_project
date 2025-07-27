from django import forms

INDIAN_STATES = [
    ('MH', 'Maharashtra'),
]

MAHARASHTRA_CITIES = [
    ('Mumbai', 'Mumbai'),
    ('Pune', 'Pune'),
    ('Nagpur', 'Nagpur'),
    ('Thane', 'Thane'),
    ('Nashik', 'Nashik'),
    ('Aurangabad', 'Aurangabad'),
    ('Solapur', 'Solapur'),
    ('Amravati', 'Amravati'),
    ('Navi Mumbai', 'Navi Mumbai'),
    ('Kolhapur', 'Kolhapur'),
    ('Akola', 'Akola'),
    ('Latur', 'Latur'),
    ('Dhule', 'Dhule'),
    ('Ahmednagar', 'Ahmednagar'),
    ('Jalgaon', 'Jalgaon'),
    ('Chandrapur', 'Chandrapur'),
    ('Parbhani', 'Parbhani'),
    ('Ichalkaranji', 'Ichalkaranji'),
    ('Jalna', 'Jalna'),
    ('Bhusawal', 'Bhusawal'),
    ('Nanded', 'Nanded'),
    ('Sangli', 'Sangli'),
    ('Beed', 'Beed'),
    ('Osmanabad', 'Osmanabad'),
    ('Panvel', 'Panvel'),
    ('Wardha', 'Wardha'),
    ('Satara', 'Satara'),
    ('Ratnagiri', 'Ratnagiri'),
    ('Gondia', 'Gondia'),
    ('Yavatmal', 'Yavatmal'),
    ('Baramati', 'Baramati'),
    ('Nandurbar', 'Nandurbar'),
    ('Hingoli', 'Hingoli'),
    ('Washim', 'Washim'),
    ('Bhandara', 'Bhandara'),
    ('Raigad', 'Raigad'),
    ('Palghar', 'Palghar'),
    ('Vasai-Virar', 'Vasai-Virar'),
    ('Malegaon', 'Malegaon'),
    ('Karad', 'Karad'),
    ('Ambarnath', 'Ambarnath'),
    ('Ulhasnagar', 'Ulhasnagar'),
    ('Kalyan', 'Kalyan'),
    ('Dombivli', 'Dombivli'),
    ('Mira-Bhayandar', 'Mira-Bhayandar'),
    ('Badlapur', 'Badlapur'),
    ('Alibag', 'Alibag'),
]

class ShippingForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    contact_number = forms.CharField(max_length=10)
    address = forms.CharField(widget=forms.Textarea)
    state = forms.ChoiceField(choices=INDIAN_STATES, initial='MH')
    city = forms.ChoiceField(choices=MAHARASHTRA_CITIES)
    pin_code = forms.CharField(max_length=6)
