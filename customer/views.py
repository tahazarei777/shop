from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Customer, Transaction
from .forms import CustomerForm
import pandas as pd
from django.http import HttpResponse
from .models import Transaction
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Alignment
from decimal import Decimal

from datetime import date, timedelta
import pandas as pd
from django.http import HttpResponse
from .models import Customer, Transaction
@login_required
def customer_dashboard(request):

    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("customer_dashboard")
    else:
        form = CustomerForm()

    customers = Customer.objects.all()

    query = request.GET.get("query")
    if query:
        customers = customers.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )

    sort_by = request.GET.get("sort_by")
    if sort_by == "amount_desc":
        customers = customers.order_by("-amount")
    elif sort_by == "amount_asc":
        customers = customers.order_by("amount")
    elif sort_by == "alpha":
        customers = customers.order_by("first_name", "last_name")

    show_paid = request.GET.get("show_paid")
    if not show_paid:
        customers = customers.filter(is_paid=False)

    total_debt = sum(c.amount for c in customers if not c.is_paid)

    context = {
        "form": form,
        "customers": customers,
        "total_debt": total_debt,
        "today_date": date.today(),
    }
    return render(request, "account/dashboard.html", context)

@login_required
def delete_customer(request, id):
    """حذف مشتری با AJAX"""
    if request.method == "POST":
        try:
            customer = Customer.objects.get(id=id)
            customer.delete()
            return JsonResponse({"success": True})
        except Customer.DoesNotExist:
            return JsonResponse({"success": False, "error": "مشتری یافت نشد"})

    return JsonResponse({"success": False, "error": "درخواست نامعتبر"})

@login_required
@csrf_exempt
def settle_customer(request, id):
    if request.method == "POST":
        data = json.loads(request.body)
        amount = Decimal(str(data.get("amount", 0)))  # تبدیل به Decimal
        operation = data.get("operation", "subtract")
        customer = Customer.objects.get(id=id)

        is_addition = operation == "add"
        if not is_addition:
            customer.amount -= amount
        else:
            customer.amount += amount

        customer.is_paid = customer.amount <= 0
        customer.save()

        # ذخیره تراکنش
        Transaction.objects.create(
            customer=customer,
            amount=amount,
            is_addition=is_addition,
            date=timezone.now(),
        )

        return JsonResponse(
            {
                "success": True,
                "new_amount": float(customer.amount),  # تبدیل Decimal به float برای JS
                "is_paid": customer.is_paid,
            }
        )
    return JsonResponse({"success": False, "error": "درخواست نامعتبر"})


import pandas as pd
from io import BytesIO
from django.http import HttpResponse
from .models import Transaction
from django.contrib.auth.decorators import login_required

@login_required
def export_excel(request):
    transactions = Transaction.objects.select_related("customer").all().order_by("date")

    data = []
    for t in transactions:
        value = t.amount if t.is_addition else -t.amount
        data.append({
            "تاریخ": t.date.strftime("%Y-%m-%d"),
            "نام مشتری": f"{t.customer.first_name} {t.customer.last_name}",
            "تغییر مبلغ": value
        })

    df = pd.DataFrame(data)

    # استفاده از BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="تراکنش‌ها")
        worksheet = writer.sheets["تراکنش‌ها"]
        for col in ["A", "C"]:  # تاریخ و تغییر مبلغ راست‌چین شوند
            for cell in worksheet[col]:
                cell.alignment = cell.alignment.copy(horizontal='right')

    output.seek(0)
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="transactions.xlsx"'
    return response
