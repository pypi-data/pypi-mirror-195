from datetime import date
from datetime import datetime as dt
from financemodule.models import Finance , FinanceAccounting , Exchangerate , Loanamount , Interestamount
from .enum import Partytype , ProgramType , ModelType , CustomerType , Accounttype
from dataclasses import dataclass 
import contextlib 
from typing import Optional



def process(request):
    return (
        request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", ""))
        .split(",")[0]
        .strip()
    )


# Create your views here.







@dataclass
class FinanceModuleHandler:

    # BASE CONSTRUCTOR #

    finance_req_id : int or str
    program_type: str
    anchor_party: str
    counterparty: str
    due_date: str
    model_type : str
    
    invoice_amount : Optional[int] = None
    finance_amount: Optional[int] = None
    repayment_amount : Optional[int] = None
    settlement_amount : Optional[int] = None
    margin : Optional[int] = None
    account_info_1 : Optional[None] = None
    account_data_1 : Optional[None] = None
    account_info_2: Optional[None] = None
    account_data_2 : Optional[None] = None
    repayment_account : Optional[int] = None
    repayment_currency : Optional[str] = None
    invoice_currency : Optional[str] = None
    finance_currency : Optional[str] = None
    settlement_currency: Optional[str] = None
    base_currency : Optional[str] = None
    interest_type : Optional[str] = None
    interest_rate_type: Optional[str] = None
    interest_paid_by : Optional[str] = None


    def __post_init__(self):
        if self.model_type == ModelType.FINANCING.value:    
            self.create_finance()
        elif self.model_type == ModelType.REPAYMENT.value:
            self.repayment()
        else:
            raise ValueError("model type must be FINANCING OR REPAYMENT")

    
    def gets_loan_amount(self):
        base_query = Loanamount.objects.get(customer = self.anchor_party , program_type = self.program_type , currency = self.finance_currency)
        return base_query.amount

    
    


    def calculated_interest_amount(self , amount ):
        interest_rate = self.margin if self.interest_type == "FIXED" else 90 + self.margin
        current_date = date.today()
        calculated_date = (
            dt.strptime(str(self.due_date), "%Y-%m-%d")
            - dt.strptime(str(current_date), "%Y-%m-%d")
        ).days
        interest_amount = (amount * interest_rate) * (calculated_date / 365)
        return interest_amount, interest_rate


    def calculated_interest_values(self):
        if self.type == ModelType.FINANCING.value and self.program_type == ProgramType.APF.value :
            # finance_currency
            if Interestamount.objects.filter(program_type=self.program_type , currency=self.finance_currency).exists():
                return self.calculated_interest_amount(amount=self.finance_amount)[0], self.finance_currency or None
            # base_currency
            elif Interestamount.objects.filter(program_type=self.program_type , currency=self.base_currency).exists():
                return self.calculated_interest_amount(amount=self.repayment_amount)[0] , self.base_currency
        if self.type == ModelType.REPAYMENT.value and self.program_type == ProgramType.APF.value:
            # repayment currency
            if Interestamount.objects.filter(program_type=self.program_type , currency=self.repayment_currency).exists():
                return self.calculated_interest_amount(amount=self.repayment_amount)[0], self.repayment_currency or None
            # base currency
            elif Interestamount.objects.filter(program_type=self.program_type , currency=self.base_currency).exists():
                return self.calculated_interest_amount(amount=self.repayment_amount)[0] , self.base_currency


    def gets_interest_amount(self):
        return Interestamount.objects.get(program_type=self.program_type , currency=self.finance_currency or self.base_currency)

    def create_finance(self):
        current_interest_amount = self.calculated_interest_amount(amount=self.finance_amount)
        calculated_amount = self.finance_amount - current_interest_amount[0]
        exchange_rate_queryset = Exchangerate.objects.get(rate_currency=self.finance_currency)
        if self.program_type != ProgramType.APF.value:
            raise ValueError("program type should be APF , RF or DF")
        finance_model = Finance.objects.create(
                finance_id = self.finance_req_id,
                finance_date = self.due_date,
                finance_request_id = self.finance_req_id,
                program_type = self.program_type,
                anchor_party = self.anchor_party,
                counterparty = self.counterparty,
                due_date = self.due_date,
                invoice_currency = self.invoice_currency,
                invoice_amount = self.invoice_amount ,
                finance_currency = self.finance_currency,
                finance_amount = self.finance_amount,
                settlement_currency = self.settlement_currency,
                settlement_amount = self.settlement_amount,
                repayment_account = self.repayment_account,
                interest_type = self.interest_type,
                interest_rate_type = self.interest_rate_type,
                margin = self.margin,
                interest_paid_by = self.interest_paid_by,
                own_party_account_info = self.account_info_1,
                remittance_info = self.account_info_2,
                status = ModelType.FINANCING.value
        )


        if self.interest_paid_by == Partytype.OWNPARTY.value:

            finance_account_query = FinanceAccounting.objects.bulk_create([

            # type DEBIT loan account
            FinanceAccounting(contract_ref = self.finance_req_id, finance_model = finance_model ,stage = ModelType.FINANCING.value ,
            type =  Accounttype.DEBIT.value , currency=self.finance_currency,amount = self.finance_amount , account = "LOAN ACCOUNT" , 
            account_type= CustomerType.customer.value,base_currency= self.base_currency ,
            exch_rate = exchange_rate_queryset.rate_mid),

            # type CREDIT remittance account
            FinanceAccounting(contract_ref = self.finance_req_id, finance_model = finance_model ,stage = ModelType.FINANCING.value,
            type = Accounttype.CREDIT.value , currency=self.finance_currency,amount= self.finance_amount, account = "REMITTANCE" , 
            account_type= CustomerType.customer.value,base_currency= self.base_currency ,
            exch_rate = exchange_rate_queryset.rate_mid),

            ])

            finance_account_query.base_currency_amount = finance_account_query.amount / exchange_rate_queryset.rate_mid
            finance_account_query.save()

            # change on_save for the base_currency_amount

        if self.interest_paid_by == Partytype.COUNTERPARTY.value:

            FinanceAccounting.objects.bulk_create([

            # type DEBIT (loan account)
            FinanceAccounting(contract_ref = self.finance_req_id, finance_model = finance_model ,stage = ModelType.FINANCING.value , 
            type =  Accounttype.DEBIT.value  , currency=self.finance_currency,amount=self.finance_amount , account = "LOAN ACCOUNT" , 
            account_type= CustomerType.customer.value,base_currency= self.base_currency,
            base_currency_amount= self.finance_amount / exchange_rate_queryset.rate_mid,
            exch_rate = exchange_rate_queryset.rate_mid),

            # type CREDIT (amount less interest account)
            FinanceAccounting(contract_ref = self.finance_req_id, finance_model = finance_model  ,stage = ModelType.FINANCING.value,
            type =  Accounttype.CREDIT.value  , currency = self.finance_currency,amount = calculated_amount, account = self.account_data_2 , 
            account_type= CustomerType.customer.value,base_currency= self.base_currency,
            base_currency_amount= calculated_amount / exchange_rate_queryset.rate_mid,
            exch_rate = exchange_rate_queryset.rate_mid),

            # credit interest amount
            FinanceAccounting(contract_ref = self.finance_req_id, finance_model = finance_model  ,stage = ModelType.FINANCING.value,
            type =  Accounttype.CREDIT.value  , currency = self.calculated_interest_values()[1] , 
            amount = self.calculated_interest_values()[0], 
            account = self.gets_interest_amount().account , 
            account_type= CustomerType.internal.value , base_currency= self.base_currency,
            base_currency_amount = self.calculated_interest_values()[0] if self.base_currency == self.calculated_interest_values()[1] 
            else self.calculated_interest_values()[0] /  exchange_rate_queryset.rate_mid,
            exch_rate = exchange_rate_queryset.rate_mid),

            ])

        return current_interest_amount



    def repayment(self):

        current_interest_amount = self.calculated_interest_amount(amount=self.repayment_amount)
        calculated_amount = self.repayment_amount + current_interest_amount[0]
        if self.program_type != ProgramType.APF.value:
            raise ValueError("program type should be APF , RF or DF")
        finance_model = Finance.objects.update_or_create(
                finance_id = self.finance_req_id,
                finance_request_id = self.finance_req_id,
                defaults={
                    "program_type" : self.program_type,
                    "finance_date": self.due_date,
                    "due_date": self.due_date,
                    "invoice_currency": self.invoice_currency,
                    "invoice_amount": self.invoice_amount,
                    "finance_currency": self.finance_currency,
                    "finance_amount": self.finance_amount,
                    "settlement_currency": self.settlement_currency,
                    "repayment_currency" : self.repayment_currency,
                    "repayment_account": self.repayment_account,
                    "interest_type": self.interest_type,
                    "interest_rate_type": self.interest_rate_type,
                    "margin": self.margin,
                    "interest_paid_by": self.interest_paid_by,
                    "own_party_account_info": self.account_info_1,
                    "remittance_info":  self.account_info_2,
                    "status": ModelType.REPAYMENT.value
                }
            )
        
        if self.interest_paid_by == Partytype.OWNPARTY.value:
                
               
                FinanceAccounting.objects.bulk_create([
                
                # type DEBIT repayment account
                FinanceAccounting(contract_ref = self.finance_req_id, finance_model = finance_model ,stage = ModelType.REPAYMENT.value ,
                type =  Accounttype.DEBIT.value , currency=self.repayment_currency,
                amount = calculated_amount, 
                account = self.repayment_account , 
                account_type= CustomerType.customer.value,base_currency= self.base_currency ,
                base_currency_amount =  calculated_amount / exchange_rate_queryset.rate_mid,
                exch_rate = exchange_rate_queryset.rate_mid),

                # type CREDIT loan account
                FinanceAccounting(contract_ref = self.finance_req_id, finance_model = finance_model ,stage = ModelType.REPAYMENT.value,
                type = Accounttype.CREDIT.value , currency=self.repayment_currency,amount= self.repayment_amount, account = "LOAN ACCOUNT" , 
                account_type= CustomerType.customer.value,base_currency= self.base_currency ,
                base_currency_amount= self.repayment_amount / exchange_rate_queryset.rate_mid,
                exch_rate = exchange_rate_queryset.rate_mid),


                # credit interest amount
                FinanceAccounting(contract_ref = self.finance_req_id, finance_model = finance_model  ,stage = ModelType.REPAYMENT.value,
                type =  Accounttype.CREDIT.value  , currency = self.calculated_interest_values()[1] , 
                amount = self.calculated_interest_values()[0], 
                account = self.gets_interest_amount().account , 
                account_type= CustomerType.internal.value , base_currency= self.base_currency,
                base_currency_amount = self.calculated_interest_values()[0] if self.base_currency == self.calculated_interest_values()[1] 
                else self.calculated_interest_values()[0] / exchange_rate_queryset.rate_mid,
                exch_rate = exchange_rate_queryset.rate_mid),
                
                ])

                # change on_save for the base_currency_amount

        if self.interest_paid_by == Partytype.COUNTERPARTY.value:
                
                FinanceAccounting.objects.bulk_create([
                
                # type DEBIT finance amount
                FinanceAccounting(contract_ref = self.finance_req_id, finance_model = finance_model ,stage = ModelType.REPAYMENT.value ,
                type =  Accounttype.DEBIT.value , currency=self.repayment_currency,
                amount = self.repayment_amount , 
                account = self.repayment_account , 
                account_type= CustomerType.customer.value,base_currency= self.base_currency ,
                base_currency_amount= self.repayment_amount / exchange_rate_queryset.rate_mid,
                exch_rate = exchange_rate_queryset.rate_mid),

                # type CREDIT finance amount
                FinanceAccounting(contract_ref = self.finance_req_id, finance_model = finance_model ,stage = ModelType.REPAYMENT.value,
                type = Accounttype.CREDIT.value , currency=self.repayment_currency,amount= self.repayment_amount, account = "LOAN ACCOUNT" , 
                account_type= CustomerType.customer.value,base_currency= self.base_currency ,
                base_currency_amount= self.repayment_amount / exchange_rate_queryset.rate_mid,
                exch_rate = exchange_rate_queryset.rate_mid),

            
                ])

        return current_interest_amount





from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response


class testapiview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request, *args, **kwargs):

        financing_module_handler = FinanceModuleHandler(
            finance_req_id = 1,
            program_type = "APF",
            anchor_party = "1",
            counterparty = "2" ,
            due_date = "2023-03-28",
            model_type = "FINANCING",
            invoice_currency = "USD" , 
            finance_currency = "USD" ,
            base_currency = "AED" , 
            invoice_amount = 1234,
            finance_amount = 1213,
            settlement_amount = 2525252,
            account_info_1 = {"test" : "test"},
            account_info_2 = {"test" : "test"},
            account_data_1 = "test" ,
            account_data_2 = "test2" ,
            interest_type = "FIXED" , 
            interest_rate_type = "FLOATING", 
            margin = 90 ,
            interest_paid_by="ownparty"
        )
        data  = financing_module_handler.create_finance()
        print(round(data[0]))
        print(data[1])
        return Response({"status": "SUCCESS", "data": "data" })
        