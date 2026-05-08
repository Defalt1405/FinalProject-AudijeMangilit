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

def payslips(request): # Hyde added "Payslip Creation Functionality"
    employee_objects = Employee.objects.all()
    message = None
    payslipobjects = Payslip.objects.all()

    if request.method == "POST":

        emplocheck = request.POST.get("payroll_for")
        if emplocheck == "all":
            message = "Can only create payslips per employee. Select an ID number and try again."
        else:
            # information from POST method
            employeeguy = Employee.objects.get(pk=emplocheck)
            month = request.POST.get("month")
            year = request.POST.get("year")
            cycle = request.POST.get("cycle")

            # information from Employee object
            curemplo_rate = employeeguy.getRate()
            curemplo_allow = employeeguy.getAllowance()
            curemplo_ot = employeeguy.getOvertime()
            
            # other
            pagibig = 100
            philhealth = curemplo_rate * 0.04
            sss = curemplo_rate * 0.045

            # cycle calculation
            priorcycle = (curemplo_rate/2) + curemplo_allow + curemplo_ot
            if cycle == "1":
                curdaterange = "1-15"
                taxcalc1 = (priorcycle - pagibig)
            elif cycle == "2":
                if month == "February":
                    curdaterange = "16-28"
                elif month == "April" or month == "June" or month == "September" or month == "November":
                    curdaterange = "16-30"
                else:
                    curdaterange = "16-31"
                taxcalc1 = (priorcycle - philhealth - sss)
            tax = taxcalc1 * 0.2
            totalpay = taxcalc1 - tax

            # create payslip object with the above information
            Payslip.objects.create(
                id_number = employeeguy,
                month = month,
                date_range = curdaterange,
                year = year,
                pay_cycle = cycle,
                rate = curemplo_rate,
                earnings_allowance = curemplo_allow,
                deductions_tax = tax,
                deductions_health = philhealth,
                pag_ibig = pagibig,
                sss = sss,
                overtime = curemplo_ot,
                total_pay = totalpay
            )

            Employee.objects.filter(pk=emplocheck).update(overtime_pay="0")

    return render(request, 'payroll_app/payslips.html', {'emp':employee_objects, "message":message, "psl":payslipobjects})

def view_payslip(request, pk): # created by Hyde
    curpayslip = get_object_or_404(Payslip, pk=pk)

    grosspay = curpayslip.getRate() + curpayslip.getEarnings_allowance() + curpayslip.getOvertime()
    
    if curpayslip.getPay_cycle() == "1":
        totaldeduct = curpayslip.getDeductions_tax() + curpayslip.getPag_ibig()
    elif curpayslip.getPay_cycle() == "2":
        totaldeduct = curpayslip.getDeductions_tax() + curpayslip.getDeductions_health() + curpayslip.getSSS()

    return render(request, "payroll_app/view_payslip.html", {"p":curpayslip, "grosspay":grosspay, "totaldeduct":totaldeduct})