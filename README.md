Current progress:

1. Models - done
2. Base html - done
3. Login page - NOT DONE X
4. Employee page - done*
5. Create employee page - done*  
6. Update employee page - done*
7. Payslips page - done*
8. View payslips page - NOT DONE X

*debugging needed

Login specs:
- The final project web app should have a login page
- When no one is logged in, all urls should go to the login page
- When an admin is logged in, all features are available as normal
- When an employee is logged in, only two pages are available:  (1) Payslips page, but only the payslips of that employee (2) View Payslip page

Notes:
- Debugging is still generally not done, especially when it comes to all the forms. Make sure all forms have a maximum input length, negative number error handling and anything else to reduce debugging during defense
- Make sure the columns have a maximum decimal display (ex.: overtime can sometimes display like 7 decimal places, limit to 1 or 2), so it looks better
- Most of the views and urls will need to be edited slightly for when login functionality is created
- potential idea for login: create a separate admin model, use a global variable for redirecting the user

Notes from Hyde:
- attempted to check payslips page after adding views functionality and payslips table data for payslips.html and it displayed the raw html despite saving the data? unsure how to debug this. (May 8, 8:35pm)
- finally got payslips.html to work, but no views/functionality/template for view_payslips yet (May 8, 10:02pm)