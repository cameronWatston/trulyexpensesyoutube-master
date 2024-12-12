from django.shortcuts import render
from expenses.models import Expense
from userincome.models import UserIncome
from django.db.models import Sum
from datetime import date, timedelta
import calendar
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def dashboard(request):
    today = date.today()
    date_range = request.GET.get('date_range', 'this_month')
    start_date = None
    end_date = today

    if date_range == 'last_month':
        first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        last_day_last_month = first_day_last_month.replace(day=calendar.monthrange(first_day_last_month.year, first_day_last_month.month)[1])
        start_date = first_day_last_month
        end_date = last_day_last_month
    elif date_range == 'last_30_days':
        start_date = today - timedelta(days=30)
    else:  # this_month
        start_date = today.replace(day=1)

    # Total income and expenses
    total_income = UserIncome.objects.filter(owner=request.user, date__range=(start_date, end_date)).aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = Expense.objects.filter(owner=request.user, date__range=(start_date, end_date)).aggregate(total=Sum('amount'))['total'] or 0

    carryover = total_income - total_expenses

    # Expenses by category
    category_data = (
        Expense.objects.filter(owner=request.user, date__range=(start_date, end_date))
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    categories = [entry['category'] for entry in category_data]
    category_totals = [entry['total'] for entry in category_data]

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'carryover': carryover,
        'categories': categories,
        'category_totals': category_totals,
        'selected_range': date_range,
    }

    return render(request, 'dashboard/dashboard.html', context)

from .forms import MonthlyFinanceForm
from .models import MonthlyFinance

from decimal import Decimal

@login_required
def debt_savings_calculator(request):
    # Check if there's an existing entry for the user for the current month
    monthly_finance, created = MonthlyFinance.objects.get_or_create(user=request.user)

    # Calculate the carryover (assuming it's already calculated as a float)
    carryover = Decimal(request.session.get("carryover", 0))

    # If it's a GET request, render the form
    if request.method == "POST":
        form = MonthlyFinanceForm(request.POST, instance=monthly_finance)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = MonthlyFinanceForm(instance=monthly_finance)

    # Calculate remaining amount after savings
    savings_goal = monthly_finance.savings_goal or Decimal(0)
    remaining_after_savings = carryover - savings_goal

    # Render the template with the form and calculations
    context = {
        "form": form,
        "carryover": carryover,
        "savings_goal": savings_goal,
        "remaining_after_savings": remaining_after_savings,
    }
    return render(request, "dashboard/debt_savings_calculator.html", context)
