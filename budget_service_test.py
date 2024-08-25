import unittest
import datetime
from unittest.mock import patch

from budget_service import Budget, BudgetService


class BudgetServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.budget_service = BudgetService()
        get_budgets_patcher = patch('budget_service.get_budgets')
        self.fake_get_budgets = get_budgets_patcher.start()
        self.fake_get_budgets.return_value = [
            Budget("202405", 310),
            Budget("202406", 300),
            Budget("202407", 310),
            Budget("202408", 310),
            Budget("202505", 310),
            Budget("202508", 310),
        ]

    def test_invalid_input(self):
        start = datetime.date(2024, 5, 1)
        end = datetime.date(2024, 4, 1)
        self.total_amount_should_be(0, start, end)

    def test_single_day(self):
        start = datetime.date(2024, 5, 1)
        end = datetime.date(2024, 5, 1)
        self.total_amount_should_be(10, start, end)

    def test_partial_month(self):
        start = datetime.date(2024, 5, 1)
        end = datetime.date(2024, 5, 10)
        self.total_amount_should_be(100, start, end)

    def test_whole_month(self):
        start = datetime.date(2024, 5, 1)
        end = datetime.date(2024, 5, 31)
        self.total_amount_should_be(310, start, end)

    def test_cross_month(self):
        start = datetime.date(2024, 5, 31)
        end = datetime.date(2024, 6, 2)
        self.total_amount_should_be(30, start, end)

    def test_cross_three_month(self):
        start = datetime.date(2024, 5, 31)
        end = datetime.date(2024, 7, 2)
        self.total_amount_should_be(330, start, end)

    def test_cross_year(self):
        start = datetime.date(2024, 7, 31)
        end = datetime.date(2025, 8, 31)
        self.total_amount_should_be(940, start, end)

    def total_amount_should_be(self, expected, start, end):
        self.assertEqual(expected, self.budget_service.get_total_amount(start, end))


if __name__ == '__main__':
    unittest.main()
