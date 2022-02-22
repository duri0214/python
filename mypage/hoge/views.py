import datetime
from django.shortcuts import get_object_or_404
from django.views import generic

from .forms import AddTaskForm
from .models import Store, Staff, Schedule
from django.utils import timezone
from django.db.models import Q

PUBLIC_HOLIDAYS = [
    # 2022
    datetime.date(year=2022, month=1, day=1),
    datetime.date(year=2022, month=1, day=10),
    datetime.date(year=2022, month=2, day=11),
    datetime.date(year=2022, month=2, day=23),
    datetime.date(year=2022, month=3, day=21),
    datetime.date(year=2022, month=4, day=29),
    datetime.date(year=2022, month=5, day=3),
    datetime.date(year=2022, month=5, day=4),
    datetime.date(year=2022, month=5, day=5),
    datetime.date(year=2022, month=7, day=18),
    datetime.date(year=2022, month=8, day=11),
    datetime.date(year=2022, month=9, day=19),
    datetime.date(year=2022, month=9, day=23),
    datetime.date(year=2022, month=10, day=10),
    datetime.date(year=2022, month=11, day=3),
    datetime.date(year=2022, month=11, day=23),
]


class StoreList(generic.ListView):
    model = Store
    ordering = 'name'


class StaffList(generic.ListView):
    model = Staff
    ordering = 'name'

    store = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['store'] = self.store
        return context

    def get_queryset(self):
        store = self.store = get_object_or_404(Store, pk=self.kwargs['pk'])
        queryset = super().get_queryset().filter(store=store)
        return queryset


class StaffCalendar(generic.TemplateView):
    template_name = 'hoge/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff = get_object_or_404(Staff, pk=self.kwargs['pk'])
        today = datetime.date.today()

        # どの日を基準にカレンダーを表示するかの処理。
        # 年月日の指定があればそれを、なければ今日からの表示。
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)
        else:
            base_date = today

        # カレンダーは1週間分表示するので、基準日から1週間の日付を作成しておく
        days = [base_date + datetime.timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]

        # 9時から17時まで1時間刻み、1週間分の、値がTrueなカレンダーを作る
        calendar = {}
        for hour in range(9, 18):
            row = {}
            for day in days:
                row[day] = True
            calendar[hour] = row

        # カレンダー表示する最初と最後の日時の間にある予約を取得する
        start_time = datetime.datetime.combine(start_day, datetime.time(hour=9, minute=0, second=0))
        end_time = datetime.datetime.combine(end_day, datetime.time(hour=17, minute=0, second=0))
        for schedule in Schedule.objects.filter(staff=staff).exclude(Q(start__gt=end_time) | Q(end__lt=start_time)):
            local_dt = timezone.localtime(schedule.start)
            booking_date = local_dt.date()
            booking_hour = local_dt.hour
            if booking_hour in calendar and booking_date in calendar[booking_hour]:
                calendar[booking_hour][booking_date] = False

        context['staff'] = staff
        context['calendar'] = calendar
        context['days'] = days
        context['start_day'] = start_day
        context['end_day'] = end_day
        context['before'] = days[0] - datetime.timedelta(days=7)
        context['next'] = days[-1] + datetime.timedelta(days=1)
        context['today'] = today
        context['public_holidays'] = PUBLIC_HOLIDAYS
        context['add_task_form'] = AddTaskForm
        return context
