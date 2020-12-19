from calendar import monthrange
from datetime import date, datetime

from dateutil.relativedelta import relativedelta
import xlwt

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from print_edition.models import PrintEdition
from subscription.forms import RequestCreateForm
from subscription.models import Request, Subscription


@login_required(login_url='login')
def create_request(request):
    if request.method == 'POST':
        request_form = RequestCreateForm(request.POST)
        if request_form.is_valid():
            new_request = request_form.save(commit=False)
            new_request.user = request.user
            new_request.save()
            return render(request, 'request_created.html')
    else:
        request_form = RequestCreateForm()
    return render(request, 'request.html', {'request_form': request_form})


@login_required(login_url='login')
def approve(request, request_id):
    if request.method == 'POST':
        start_of_month = date(year=date.today().year, month=date.today().month, day=1)

        request_object = Request.objects.get(id=request_id)

        request_object.is_approved = True
        request_object.save()

        Subscription.objects.create(
            print_edition_id=request_object.print_edition_id,
            user_id=request_object.user_id,
            duration=request_object.duration,
            start_date=start_of_month + relativedelta(months=1),
            end_date=start_of_month + relativedelta(months=request_object.duration + 1),
        )

    return HttpResponse()


@login_required(login_url='login')
def get_requests(request):
    if request.user.is_staff:
        return render(
            request,
            'staff_requests_table.html',
            {'requests': Request.objects.filter(is_approved=False).select_related('user', 'print_edition').all()}
        )
    return render(
        request,
        'user_requests_table.html',
        {'requests': Request.objects.filter(user_id=request.user.id).select_related('print_edition').all()}
    )


@login_required(login_url='login')
def get_report(request):
    return render(request, 'report.html')


@login_required(login_url='login')
def get_month_subscriptions(request):
    now = date.today()

    return render(
        request,
        'subscriptions_table.html',
        {
            'subscriptions': Subscription.objects.filter(
                end_date__gte=date(year=now.year, month=now.month, day=1),
                end_date__lte=date(year=now.year, month=now.month, day=monthrange(now.year, now.month)[1])
            ).select_related('user', 'print_edition').all()
        }
    )


class Report:
    header_cell_style = xlwt.easyxf('align: horiz center, vert center; font: bold true')
    data_cell_style = xlwt.easyxf('align: horiz center, vert center;')

    @classmethod
    def _init_table(cls):
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet(f'Ведомость')

        worksheet.col(0).width = 256 * 20
        worksheet.col(1).width = 256 * 20
        worksheet.col(2).width = 256 * 15
        worksheet.col(3).width = 256 * 15
        worksheet.col(4).width = 256 * 18
        worksheet.col(5).width = 256 * 20
        worksheet.col(6).width = 256 * 10
        worksheet.col(7).width = 256 * 10
        worksheet.col(8).width = 256 * 10

        worksheet.write(0, 0, 'Издание', style=cls.header_cell_style)
        worksheet.write(0, 1, 'Начало подписки', style=cls.header_cell_style)
        worksheet.write(0, 2, 'Срок подписки', style=cls.header_cell_style)
        worksheet.write(0, 3, 'Цена за месяц', style=cls.header_cell_style)
        worksheet.write(0, 4, 'Цена за подписку', style=cls.header_cell_style)
        worksheet.write(0, 5, 'Адрес', style=cls.header_cell_style)
        worksheet.write(0, 6, 'Фамилия', style=cls.header_cell_style)
        worksheet.write(0, 7, 'Имя', style=cls.header_cell_style)
        worksheet.write(0, 8, 'Отчество', style=cls.header_cell_style)

        return workbook, worksheet

    @classmethod
    def _fill_row(cls, worksheet, row_number, data):
        worksheet.write(row_number, 1, data['start_date'].strftime('%Y-%m-%d'), style=cls.data_cell_style)
        worksheet.write(row_number, 2, data['duration'], style=cls.data_cell_style)
        worksheet.write(row_number, 3, data['print_edition__price'], style=cls.data_cell_style)
        worksheet.write(row_number, 4, data['duration'] * data['print_edition__price'], style=cls.data_cell_style)
        worksheet.write(row_number, 5, data['user__address'], style=cls.data_cell_style)
        worksheet.write(row_number, 6, data['user__last_name'], style=cls.data_cell_style)
        worksheet.write(row_number, 7, data['user__first_name'], style=cls.data_cell_style)
        worksheet.write(row_number, 8, data['user__middle_name'], style=cls.data_cell_style)

    @classmethod
    def report(cls, request):
        if request.method == 'POST':
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')

            current_row = 0
            profit = 0
            workbook, worksheet = cls._init_table()

            for print_edition in PrintEdition.objects.filter(
                    subscriptions_query__start_date__gte=datetime.strptime(start_date, '%Y-%m-%d'),
                    subscriptions_query__start_date__lte=datetime.strptime(end_date, '%Y-%m-%d'),
            ).distinct().all():
                print_edition_profit = 0
                rows = print_edition.get_report_data(start_date, end_date)

                worksheet.write_merge(
                    current_row + 1, current_row + len(rows), 0, 0,
                    rows[0]['print_edition__name'],
                    style=cls.data_cell_style
                )

                for row in rows:
                    current_row += 1
                    print_edition_profit += row['duration'] * row['print_edition__price']

                    cls._fill_row(worksheet, current_row, row)

                current_row += 1
                profit += print_edition_profit

                worksheet.write_merge(current_row, current_row, 6, 7, 'Прибыль издания:', style=cls.header_cell_style)
                worksheet.write(current_row, 8, print_edition_profit, style=cls.data_cell_style)

                current_row += 1

            worksheet.write_merge(current_row + 2, current_row + 2, 6, 7, 'Общая прибыль:', style=cls.header_cell_style)
            worksheet.write(current_row + 2, 8, profit, style=cls.data_cell_style)

            file_name = f'Ведомость__{start_date}_{end_date}.xls'
            workbook.save(f'{settings.MEDIA_ROOT}/{file_name}')

            return JsonResponse({'file': file_name})

        return HttpResponse()
