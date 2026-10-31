import unittest
from config import calculate_price, CAR_CLASSES, SERVICES


class TestCalculatorLogic(unittest.TestCase):
    def test_polishing_business_class(self):
        """Проверка примера из ТЗ: Полировка для бизнес-класса -> от 22 000 руб."""
        res = calculate_price("business", "polishing")
        self.assertEqual(res["car_name"], "Бизнес / Кроссовер")
        self.assertEqual(res["price"], 22000)
        self.assertEqual(res["formatted_price"], "от 22 000 руб.")
        self.assertEqual(res["duration"], "1.5–2 дня")

    def test_all_combinations(self):
        """Проверка корректности расчета для всех классов и услуг."""
        for car_key, car_info in CAR_CLASSES.items():
            for service_key, service_info in SERVICES.items():
                res = calculate_price(car_key, service_key)
                self.assertGreater(res["price"], 0)
                self.assertTrue(res["formatted_price"].startswith("от "))
                self.assertIn("руб.", res["formatted_price"])
                self.assertTrue(len(res["duration"]) > 0)

    def test_multiplier_effect(self):
        """Цена на внедорожник должна быть выше, чем на малый класс."""
        res_small = calculate_price("small", "ceramic")
        res_suv = calculate_price("suv", "ceramic")
        self.assertGreater(res_suv["price"], res_small["price"])


if __name__ == "__main__":
    unittest.main()
