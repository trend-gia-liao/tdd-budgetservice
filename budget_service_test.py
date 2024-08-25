import unittest
import datetime

from budget_service import BudgetService


class BudgetServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.budget_service = BudgetService()

    def test_invalid_input(self):
        start = datetime.date(2024, 5, 1)
        end = datetime.date(2024, 4, 1)
        res = self.budget_service.get_total_amount(start, end)
        self.assertEqual(0, res)  # add assertion here

    def test_single_day(self):
        start = datetime.date(2024, 5, 1)
        end = datetime.date(2024, 5, 1)
        res = self.budget_service.get_total_amount(start, end)
        self.assertEqual(10, res)

    def test_partial_month(self):
        start = datetime.date(2024, 5, 1)
        end = datetime.date(2024, 5, 10)
        res = self.budget_service.get_total_amount(start, end)
        self.assertEqual(100, res)

    def test_whole_month(self):
        start = datetime.date(2024, 5, 1)
        end = datetime.date(2024, 5, 31)
        res = self.budget_service.get_total_amount(start, end)
        self.assertEqual(310, res)

    def test_cross_month(self):
        start = datetime.date(2024, 5, 31)
        end = datetime.date(2024, 6, 2)
        res = self.budget_service.get_total_amount(start, end)
        self.assertEqual(30, res)

    def test_cross_three_month(self):
        start = datetime.date(2024, 5, 31)
        end = datetime.date(2024, 7, 2)
        res = self.budget_service.get_total_amount(start, end)
        self.assertEqual(330, res)

    def test_cross_year(self):
        start = datetime.date(2024, 7, 31)
        end = datetime.date(2025, 8, 31)
        res = self.budget_service.get_total_amount(start, end)
        self.assertEqual(940, res)


if __name__ == '__main__':
    unittest.main()
