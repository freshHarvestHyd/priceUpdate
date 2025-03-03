from django import forms
from datetime import date

class FruitPriceForm(forms.Form):
    FRUIT_NAMES = [
        'Watermelon',
        'Muskmelon',
        'Green Grape',
        'Black Grape',
        'Mosambi',
        'Orange',
        'Papaya',
        'Pineapple',
        'Sapota',
        'Pomegranate',
        'Apple'
    ]
    date = forms.DateField(
        initial=date.today,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    # Fields for default fruits
    for fruit in FRUIT_NAMES:
        locals()[f'price_{fruit.lower().replace(" ", "_")}'] = forms.DecimalField(
            max_digits=7,  # Increased to 7 digits
            decimal_places=2,
            required=False,
            label=f'Price for {fruit}'
        )
        locals()[f'unit_{fruit.lower().replace(" ", "_")}'] = forms.ChoiceField(
            choices=[
                ('kg', 'Kg'),
                ('box', 'Box'),
                ('piece', 'Piece'),
            ],
            required=False,
            label=f'Unit for {fruit}'
        )

    # Fields for custom fruit
    custom_fruit_name = forms.CharField(
        max_length=100,
        required=False,
        label='Other Fruit Name'
    )
    custom_price = forms.DecimalField(
        max_digits=7,  # Increased to 7 digits
        decimal_places=2,
        required=False,
        label='Price for Other Fruit'
    )
    custom_unit = forms.ChoiceField(
        choices=[
            ('kg', 'Kg'),
            ('box', 'Box'),
            ('piece', 'Piece'),
        ],
        required=False,
        label='Unit for Other Fruit'
    )