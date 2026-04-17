from django import forms
from ..models import ComputeExposureParameters, DutyFactor, TransmitReceiveTime
from ..views.compute_form_services import ComputeFormServices


class ComputeExposureParametersForm(forms.ModelForm):
    """ Form to Capture Operator's RF Exposure Parameters Related to Power and Antenna Specifications """

    def __init__(self, *args, **kwargs):
        super(ComputeExposureParametersForm, self).__init__(*args, **kwargs)
        self.fields['include_calculations'].initial = True

    DUTY_FACTOR_CHOICES = [
        ('.2', 'SSB (Conversational, No Speech Processing)  [20%]'),
        ('.5', 'SSB (Conversational, No Speech Processing)  [50%]'),
        ('.4', 'CW (Conversational)  [40%]'),
        ('1', 'FM  [100%]'),
        ('1', 'AM  [100%]'),
        ('1', 'AFSK (e.g., RTTY, etc.)  [100%]'),
        ('1', 'FT4  [100%]'),
        ('1', 'FT8  [100%]'),
        ('1', 'Carrier for Tuning  [100%]'),
        ('1', 'Unknown Mode (Assume Worst Case)  [100%]')
        ]

    BAND_PLAN_CHOICES = [
        (0, 'MF/HF (1.8 MHz - 54.0 MHz)'),
        (1, 'VHF/UHF (50.0 MHz - 1,300 MHz)')
        ]

    FREQUENCY_POSITION = [
        (0, 'Lowest Frequency in Band'),
        (1, 'Center Frequency in Band'),
        (2, 'Highest Frequency in Band'),
    ]

    TRANSMIT_RECEIVE_CHOICES = list(ComputeFormServices.TRANSMIT_RECEIVE_TIME.items())

    report_description = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'custom-input'}),
        required=True,
        error_messages={'required': "Report Description is Required!"}
    )

    antenna_description = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'custom-input'}),
        required=True,
        error_messages={'required': "Antenna Description is Required!"}
    )

    antenna_gain = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'custom-input'}),
        required=True,
        error_messages={'required': "Antenna Gain Is Required!"}
    )

    ground_reflection: forms.CheckboxInput(
        attrs={'class': 'form-check-input'}
    )

    effective_power = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'custom-input'}),
        required=True,
        error_messages={'required': "Power Is Required!"}
    )

    duty_factor = forms.ChoiceField(
        choices=DUTY_FACTOR_CHOICES,
        widget=forms.Select(attrs={'class': 'custom-input select-input'}),
        required=True,
        error_messages={'required': "Duty Factor is Required!"}
    )

    transmit_time = forms.ChoiceField(
        choices=TRANSMIT_RECEIVE_CHOICES,
        widget=forms.Select(attrs={'class': 'custom-input select-input'}),
        required=True,
        error_messages={'required': "Transmit Time is Required!"}
    )

    receive_time = forms.ChoiceField(
        choices=TRANSMIT_RECEIVE_CHOICES,
        widget=forms.Select(attrs={'class': 'custom-input select-input'}),
        required=True,
        error_messages={'required': "Receive Time is Required!"}
    )

    frequency_mode = forms.ChoiceField(
        choices=BAND_PLAN_CHOICES,
        widget=forms.Select(attrs={'class': 'custom-input select-input'}),
        required=True,
        error_messages={'required': "Multi-Band Group is Required!"}
    )

    frequency_position = forms.ChoiceField(
        choices=FREQUENCY_POSITION,
        widget=forms.Select(attrs={'class': 'custom-input select-input'}),
        required=True,
        error_messages={'required': "Frequency Position is Required!"}
    )

    frequency: forms.NumberInput(
        attrs={'class': 'custom-input'}
    )

    operator_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'custom-input'}),
        required=True,
        error_messages={'required': "Operator Name is Required!"}
    )

    call_sign = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'custom-input'}),
        required=True,
        error_messages={'required': "Call Sign is Required!"}
    )

    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'custom-input'}),
        required=True,
        error_messages = {'required': "Email Address is Required!"}

    )

    include_calculations: forms.CheckboxInput(
        attrs={'class': 'form-check-input'}
    )

    class Meta:
        model = ComputeExposureParameters
        fields = [
            'report_description',
            'antenna_description',
            'antenna_gain',
            'ground_reflection',
            'effective_power',
            'duty_factor',
            'transmit_time',
            'receive_time',
            'frequency_mode',
            'frequency_position',
            'frequency',
            'operator_name',
            'call_sign',
            'email',
            'include_calculations'
        ]
