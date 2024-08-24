import calendar
import datetime
from typing import List


class Budget:
    year_month: str
    amount: int

    def __init__(self, year_month, amount):
        self.year_month = year_month
        self.amount = amount

    def get_days(self):
        first_day = self.first_day()
        return calendar.monthrange(first_day.year, first_day.month)[1]

    def daily_amount(self):
        daily_amount = self.amount / self.get_days()
        return daily_amount

    def last_day(self):
        first_day = self.first_day()
        return datetime.date(first_day.year, first_day.month, self.get_days())

    def first_day(self):
        return datetime.datetime.strptime(self.year_month, '%Y%m').date()

    def create_period(self):
        return Period(self.first_day(), self.last_day())

    def overlapping_amount(self, period):
        return self.daily_amount() * period.overlapping_days(self.create_period())


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


class Period:
    def __init__(self, start: datetime.date, end: datetime.date):
        self.start = start
        self.end = end

    def overlapping_days(self, another):
        overlapping_start = max(self.start, another.start)
        overlapping_end = min(self.end, another.end)
        return max((overlapping_end - overlapping_start).days + 1, 0)


class BudgetService:
    def get_total_amount(self, start: datetime.date, end: datetime.date):

        if start > end:
            return 0

        budgets = BudgetRepo().get_all()
        period = Period(start, end)
        return sum(map(lambda b: b.overlapping_amount(period), budgets))
