from django.shortcuts import render, redirect, get_object_or_404
from payroll_app.models import Employee, Payslip

def employees(request):
    employee_objects = Employee.objects.all()
    return render(request, 'payroll_app/employees.html', {'emp':employee_objects})

def add_overtime(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == "POST":
        hours = float(request.POST.get('overtime_hours', 0))

        #overtime calculation
        overtime_amount = (employee.rate / 160) * 1.5 * hours

        #adds to existing overtime (not replace)
        current_overtime = employee.overtime_pay or 0
        employee.overtime_pay = current_overtime + overtime_amount

        employee.save()

    return redirect('employees')

def create_employee(request):
    if request.method == "POST":
        name = request.POST.get('name')
        id_number = request.POST.get('id_number')
        rate = request.POST.get('rate')
        allowance = request.POST.get('allowance')

        if Employee.objects.filter(id_number=id_number).exists():
            return render(request, 'payroll_app/create_employee.html', {'message': 'ID Number is already in use.'})
        
        if allowance == "" or allowance is None:
            allowance = 0
        
        Employee.objects.create(
            name=name,
            id_number=id_number,
            rate=rate,
            allowance=allowance,
            overtime_pay=0
        )

        return redirect('employees')

    return render(request, 'payroll_app/create_employee.html')

def update_employee(request, pk):

    employee = get_object_or_404(Employee, pk=pk)
    message= None

    if request.method == "POST":
        name = request.POST.get('name')
        id_number = request.POST.get('id_number')
        rate = request.POST.get('rate')
        allowance = request.POST.get('allowance')

        if Employee.objects.filter(id_number=id_number).exclude(pk=employee.pk).exists():
            message = "ID Number is already in use."
        else:
            employee.name = name
            employee.id_number = id_number
            employee.rate = rate
            employee.allowance = allowance if allowance else None

            employee.save()
            return redirect('employees')

    return render(request, 'payroll_app/update_employee.html', {'employee': employee,'message': message})

def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect('employees')

def payslips(request):
    employee_objects = Employee.objects.all()
    return render(request, 'payroll_app/payslips.html', {'emp':employee_objects})
