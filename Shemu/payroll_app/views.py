from django.shortcuts import render, redirect, get_object_or_404
from payroll_app.models import Employee, Payslip, Admin

logged_in_id = 0
is_admin = False

# Account pages===============================================================================================================

def employee_login(request):
    global logged_in_id, is_admin

    error = None

    if request.method == "POST":

        id_number = request.POST.get("id_number")
        password = request.POST.get("password")

        try:
            employee = Employee.objects.get(id_number=id_number, password=password)

            logged_in_id = employee.pk
            is_admin = False

            return redirect('payslips')

        except Employee.DoesNotExist:
            error = "Invalid Employee ID or Password."

    return render(request, 'payroll_app/employee_login.html', {'error': error})

def admin_login(request):
    global logged_in_id, is_admin

    error = None

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            admin = Admin.objects.get(username=username, password=password)

            logged_in_id = admin.pk
            is_admin = True

            return redirect('employees')

        except Admin.DoesNotExist:
            error = "Invalid Username or Password."

    return render(request, 'payroll_app/admin_login.html', {'error': error})

def create_admin(request):

    error = None
    success = None

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # if passwords do not match
        if password != confirm_password:
            error = "Passwords do not match."

        # if username already exists
        elif Admin.objects.filter(username=username).exists():
            error = "Username already exists."

        else:
            Admin.objects.create(username=username, password=password)
            success = "Admin account created successfully."

    return render(request, 'payroll_app/create_admin.html', {'error': error, 'success': success})

def logout(request):
    global logged_in_id, is_admin
    logged_in_id = 0
    is_admin = False
    return redirect('employee_login')

# Employee pages================================================================

def employees(request):
    global logged_in_id, is_admin

    if logged_in_id == 0:
        return redirect('employee_login')
    
    if not is_admin:
        return redirect('payslips')

    employee_objects = Employee.objects.all()
    return render(request, 'payroll_app/employees.html', {'emp':employee_objects})

def add_overtime(request, pk):
    global logged_in_id, is_admin

    if logged_in_id == 0:
        return redirect('employee_login')
    
    if not is_admin:
        return redirect('payslips')
    
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
    global logged_in_id, is_admin

    if logged_in_id == 0:
        return redirect('employee_login')
    
    if not is_admin:
        return redirect('payslips')
    
    if request.method == "POST":
        name = request.POST.get('name')
        id_number = request.POST.get('id_number')
        password = request.POST.get('password')
        rate = request.POST.get('rate')
        allowance = request.POST.get('allowance')

        if Employee.objects.filter(id_number=id_number).exists():
            return render(request, 'payroll_app/create_employee.html', {'message': 'ID Number is already in use.'})
        
        if allowance == "" or allowance is None:
            allowance = 0
        
        Employee.objects.create(
            name=name,
            id_number=id_number,
            password=password,
            rate=rate,
            allowance=allowance,
            overtime_pay=0
        )

        return redirect('employees')

    return render(request, 'payroll_app/create_employee.html')

def update_employee(request, pk):
    global logged_in_id, is_admin

    if logged_in_id == 0:
        return redirect('employee_login')
    
    if not is_admin:
        return redirect('payslips')

    employee = get_object_or_404(Employee, pk=pk)
    message= None

    if request.method == "POST":
        name = request.POST.get('name')
        id_number = request.POST.get('id_number')
        password = request.POST.get('password')
        rate = request.POST.get('rate')
        allowance = request.POST.get('allowance')

        if Employee.objects.filter(id_number=id_number).exclude(pk=employee.pk).exists():
            message = "ID Number is already in use."
        else:
            employee.name = name
            employee.id_number = id_number
            employee.password = password
            employee.rate = rate
            employee.allowance = allowance if allowance else None

            employee.save()
            return redirect('employees')

    return render(request, 'payroll_app/update_employee.html', {'employee': employee,'message': message})

def delete_employee(request, pk):
    global logged_in_id, is_admin

    if logged_in_id == 0:
        return redirect('employee_login')
    
    if not is_admin:
        return redirect('payslips')

    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect('employees')




# Payslip pages=================================================================================================

def payslips(request): # Hyde added "Payslip Creation Functionality"
    global logged_in_id, is_admin

    if logged_in_id == 0:
        return redirect('employee_login')

    employee_objects = Employee.objects.all()
    message = None

    #loads payslips
    if is_admin:
        payslipobjects = Payslip.objects.all()
    else:
        #employee can only see their own payslips
        employee = Employee.objects.get(pk=logged_in_id)
        payslipobjects = Payslip.objects.filter(id_number=employee)

    #create payslips (admin only)
    if request.method == "POST":

        if not is_admin:
            message = "Admin access needed to create payrolls."
            return render(request, 'payroll_app/payslips.html', {'emp': employee_objects,'psl': payslipobjects,'message': message,'is_admin': is_admin})

        payroll_for = request.POST.get("payroll_for")
        month = request.POST.get("month")
        year = request.POST.get("year")
        cycle = request.POST.get("cycle")

        #all employees case
        if payroll_for == "all":

            employees = Employee.objects.all()

            for emp in employees:

                #ignore duplicate payslip
                if Payslip.objects.filter(id_number=emp,month=month,year=year,pay_cycle=cycle).exists():
                    continue

                create_payslip(emp, month, year, cycle)

        #single employee case
        else:

            emp = Employee.objects.get(pk=payroll_for)

            #duplicate check
            if Payslip.objects.filter(id_number=emp,month=month,year=year,pay_cycle=cycle).exists():
                message = "Payslip already exists for this employee."

            else:
                create_payslip(emp, month, year, cycle)

    #final render
    return render(request, 'payroll_app/payslips.html', {'emp': employee_objects,'psl': payslipobjects,'message': message,'is_admin': is_admin})

def create_payslip(emp, month, year, cycle): #sub-function for payslips(); for organization

    rate = emp.getRate()
    allowance = emp.getAllowance()
    overtime = emp.getOvertime()

    pagibig = 100
    philhealth = rate * 0.04
    sss = rate * 0.045

    base = (rate / 2) + allowance + overtime

    #CYCLE 1
    if cycle == "1":
        date_range = "1-15"
        taxable = base - pagibig
        tax = taxable * 0.2
        total = taxable - tax

    #CYCLE 2
    else:
        date_range = "16-30"
        taxable = base - philhealth - sss
        tax = taxable * 0.2
        total = taxable - tax

    Payslip.objects.create(
        id_number=emp,
        month=month,
        date_range=date_range,
        year=year,
        pay_cycle=cycle,
        rate=rate,
        earnings_allowance=allowance,
        deductions_tax=tax,
        deductions_health=philhealth,
        pag_ibig=pagibig,
        sss=sss,
        overtime=overtime,
        total_pay=total
    )

    #reset overtime after creation
    emp.overtime_pay = 0
    emp.save()

def view_payslip(request, pk): # created by Hyde
    global logged_in_id, is_admin

    if logged_in_id == 0:
        return redirect('employee_login')

    curpayslip = get_object_or_404(Payslip, pk=pk)

    #employee restriction (can only view own payslip, no pk guessing)
    if not is_admin:
        employee = Employee.objects.get(pk=logged_in_id)
        if curpayslip.id_number != employee:
            return redirect('payslips')

    #gross pay
    grosspay = ((curpayslip.rate /2) + curpayslip.earnings_allowance + curpayslip.overtime)

    #deductions (cycle-based)
    if curpayslip.pay_cycle == 1:
        totaldeduct = (curpayslip.pag_ibig +curpayslip.deductions_tax)

    else:  # cycle 2
        totaldeduct = (curpayslip.deductions_tax +curpayslip.deductions_health +curpayslip.sss)

    #net pay
    netpay = grosspay - totaldeduct

    return render(request, "payroll_app/view_payslip.html", {"p": curpayslip,"grosspay": grosspay,"totaldeduct": totaldeduct,"netpay": netpay})