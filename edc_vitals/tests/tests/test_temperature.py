from django.core.exceptions import ValidationError
from django.test import TestCase

from edc_vitals.utils import get_min_g3_fever, has_fever_gte_g3

from ..models import Temperature


class TestTemperature(TestCase):
    def test_simple_ok(self):
        obj = Temperature(temperature=37.5)
        obj.save()
        self.assertEqual(obj.temperature, 37.5)

    def test_temperature_lt_30_raises(self):
        for low_temp in [28.0, 29, 29.9]:
            with self.subTest(temperature=low_temp):
                model = Temperature.objects.create(temperature=low_temp)
                with self.assertRaises(ValidationError) as cm:
                    model.full_clean()
                self.assertIn("temperature", cm.exception.error_dict)
                self.assertIn(
                    "Ensure this value is greater than or equal to 30.",
                    str(cm.exception.error_dict.get("temperature")),
                )

    def test_30_lt_temperature_lt_45_ok(self):
        for temperature in [30, 31, 37.5, 39.3, 40, 45]:
            with self.subTest(temperature=temperature):
                model = Temperature.objects.create(temperature=temperature)
                try:
                    model.full_clean()
                except ValidationError as e:
                    self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_temperature_gt_45_raises(self):
        for high_temp in [45.1, 46, 50.0]:
            with self.subTest(temperature=high_temp):
                model = Temperature.objects.create(temperature=high_temp)
                with self.assertRaises(ValidationError) as cm:
                    model.full_clean()
                self.assertIn("temperature", cm.exception.error_dict)
                self.assertIn(
                    "Ensure this value is less than or equal to 45.",
                    str(cm.exception.error_dict.get("temperature")),
                )

    def test_has_fever_gte_g3(self):
        self.assertIsNone(has_fever_gte_g3())

        self.assertFalse(has_fever_gte_g3(temperature=37.5))
        self.assertFalse(has_fever_gte_g3(temperature=39.2))

        self.assertTrue(has_fever_gte_g3(temperature=39.3))
        self.assertTrue(has_fever_gte_g3(temperature=40))
        self.assertTrue(has_fever_gte_g3(temperature=45))

    def test_min_g3_fever(self):
        self.assertEquals(get_min_g3_fever(), 39.3)
