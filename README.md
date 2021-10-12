# demo-bank

List of APIs

loanFund CRUD : permission for bank group only 

http://localhost:8000/api/loanfund-viewset/

loanTerm CRUD : permission for bank group only 

http://localhost:8000/api/loanterm-viewset/

investor API : to search(GET) available loan fund based by amount added in body , and subscribe to a fund (PUT) with fundNumber and amount in body . permission for investor group only

http://localhost:8000/api/investorAPI/

customer API : to search(GET) available loan term based by amount added in body , and subscribe to a term (PUT) with termNumber and amount in body . permission for customer group only

http://localhost:8000/api/investorAPI/

applications API: returns (GET) the user's applications with all related info

http://localhost:8000/api/applicationsAPI/

authentication API :

http://localhost:8000/api/auth/

edit status API : for the bank personnel to edit the loan fund/term status (PUT)

http://localhost:8000/api/editFundStatusAPI/
http://localhost:8000/api/editTermStatusAPI/

amortization API : for the customer to know his monthly loan payment after entering termNumber in the body (GET)

http://localhost:8000/api/amortizationAPI/


