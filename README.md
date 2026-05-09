Current progress:

1. Models - done
2. Base html - done
3. Login page - done
4. Employee page - done
5. Create employee page - done
6. Update employee page - done
7. Payslips page - done
8. View payslips page - done

Login specs:
- The final project web app should have a login page
- When no one is logged in, all urls should go to the login page
- When an admin is logged in, all features are available as normal
- When an employee is logged in, only two pages are available:  (1) Payslips page, but only the payslips of that employee (2) View Payslip page

Notes:
- final working version uploaded, final bug check needed then we done
- I also edited the payslip view to have a subfunction, for organization

Notes from Hyde:
- attempted to check payslips page after adding views functionality and payslips table data for payslips.html and it displayed the raw html despite saving the data? unsure how to debug this. (May 8, 8:35pm)
- finally got payslips.html to work, but no views/functionality/template for view_payslips yet (May 8, 10:02pm)
- payslips template (and its associated urls.py and views.py functionality) completed! view_payslip and data added as well. formatting is missing, though. (May 8, 10:49pm)
- view_payslip works except when trying to display the total deductions for absolutely no reason. can't figure it out (May 9, 12:29am)
- functionality for payslips.html and view_payslip.html completed, but not debugged yet. (May 9, 12:43am) 
- after Basti debugged, haven't touched anything else yet. payslips information isn't lining up... (May 9, 2:38)
- fixed payslip net totals not matching (May 9, 3:01pm)