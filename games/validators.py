from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

@deconstructible
class LengthRangeValidator:
    def __init__(self, min, max):
        self.max = max
        self.min = min

    def __call__(self, value):
        if len(value) > self.max:
            raise ValidationError(f'value is longer than {self.max}')
        elif len(value) < self.min:
            raise ValidationError(f'value is shorter than {self.min}')


@deconstructible
class MinMaxValidator:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def __call__(self, value):
        if value > self.max or value < self.min:
            raise ValidationError(f'{value} is not in range {self.min}-{self.max}')
