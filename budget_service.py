import calendar
import datetime
from typing import List

from dateutil.relativedelta import relativedelta


def get_single_day_amount(year, month):
    start_year_month = "{:04d}{:02d}".format(year, month)
    records = BudgetRepo().get_all()
    for record in records:
        if record.year_month == start_year_month:
            month_total_days = record.get_days()
            return record.amount / month_total_days

    return 0


class BudgetService:
    def get_total_amount(self, start: datetime.date, end: datetime.date):

        if start > end:
            return 0

        if start.year == end.year and start.month == end.month:
            return get_single_day_amount(start.year, start.month) * (end.day - start.day + 1)

        total_amount = 0

        current_date = start
        end_month = datetime.date(end.year, end.month, 1)+relativedelta(months=1)
        budgets = BudgetRepo().get_all()
        while current_date < end_month:
            budget = next(filter(lambda b: b.year_month == current_date.strftime('%Y%m'), budgets), None)
            if budget is not None:
                if current_date.strftime('%Y%m') == start.strftime('%Y%m'):
                    daily_amount = budget.daily_amount()
                    overlapping_days = budget.get_days() - start.day + 1
                elif current_date.strftime('%Y%m') == end.strftime('%Y%m'):
                    daily_amount = get_single_day_amount(end.year, end.month)
                    overlapping_days = end.day
                else:
                    daily_amount = get_single_day_amount(current_date.year, current_date.month)
                    overlapping_days = budget.get_days()
                overlapping_amount = daily_amount * overlapping_days
                total_amount += overlapping_amount
            current_date += relativedelta(months=1)

        return total_amount


class Budget:
    year_month: str
    amount: int

    def __init__(self, year_month, amount):
        self.year_month = year_month
        self.amount = amount

    def get_days(self):
        first_day = datetime.datetime.strptime(self.year_month, '%Y%m').date()
        return calendar.monthrange(first_day.year, first_day.month)[1]

    def daily_amount(self):
        daily_amount = self.amount / self.get_days()
        return daily_amount


class BudgetRepo:
    def get_all(self) -> List[Budget]:
        return [
            Budget("202405", 310),
            Budget("202406", 300),
            Budget("202407", 310),
            Budget("202408", 310),
            Budget("202505", 310),
            Budget("202508", 310),
        ]
