from django.shortcuts import render, redirect, get_object_or_404
from payroll_app.models import Employee, Payslip

def employees(request):
    employee_objects = Employee.objects.all()
    return render(request, 'payroll_app/employees.html', {'emp':employee_objects})