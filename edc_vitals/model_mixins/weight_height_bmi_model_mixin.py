from django.db import models
from edc_model import models as edc_models
from edc_reportable import calculate_bmi


class WeightHeightBmiModelMixin(models.Model):

    lower_bmi_value = 15.0

    upper_bmi_value = 60.0

    weight = edc_models.WeightField(null=True, blank=True)

    height = edc_models.HeightField(null=True, blank=True)

    calculated_bmi_value = models.DecimalField(
        verbose_name="BMI",
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=False,
        help_text="system calculated",
    )

    def save(self, *args, **kwargs):
        bmi = self.calculate_bmi()
        self.calculated_bmi_value = bmi.value if bmi else None
        super().save(*args, **kwargs)

    def calculate_bmi(self):
        return calculate_bmi(
            weight_kg=self.weight,
            height_cm=self.height,
            lower_bmi_value=self.lower_bmi_value,
            upper_bmi_value=self.upper_bmi_value,
        )

    class Meta:
        abstract = True