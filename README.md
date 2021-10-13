# demo-bank

List of APIs

loanFund CRUD : permission for bank group only 

http://localhost:8000/api/loanfund-viewset/

loanTerm CRUD : permission for bank group only 

http://localhost:8000/api/loanterm-viewset/

investor API : to search(GET) to see the investor's fund applications, and subscribe to a fund (POST) with "type" for the fund the user wants to subscribe to and "amount" in body. Permission for investor group only.

http://localhost:8000/api/investorAPI/

customer API : to search(GET) to see the cutomer loan applications,and subscribe to a fund (POST) with "type" for the fund the user wants to subscribe to and "amount" in body. Permission for customer group only.

http://localhost:8000/api/investorAPI/

applications API: returns (GET) the user's applications with all related info.

http://localhost:8000/api/applicationsAPI/

authentication API :

http://localhost:8000/api/auth/

edit status API : for the bank personnel to edit the loan fund/term status (PUT). By adding the fundNumber/termNumber in the body and the new status.

http://localhost:8000/api/editFundStatusAPI/
http://localhost:8000/api/editTermStatusAPI/

amortization API : for the customer to know his monthly loan payment after entering termNumber in the body (GET).

http://localhost:8000/api/amortizationAPI/


