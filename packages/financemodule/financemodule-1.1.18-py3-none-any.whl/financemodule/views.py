from datetime import date
from datetime import datetime as dt

from financemodule.models import Finance , FinanceAccounting , Exchangerate
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
    type : str
    invoice_currency : Optional[str] = None
    finance_currency : Optional[str] = None
    settlement_currency: Optional[str] = None
    base_currency : Optional[str] = None
    invoice_amount : Optional[int] = None
    finance_amount: Optional[int] = None
    settlement_amount : Optional[int] = None
    account_info_1 : Optional[None] = None
    account_data_1 : Optional[None] = None
    account_info_2: Optional[None] = None
    account_data_2 : Optional[None] = None
    repayment_account : Optional[int] = None
    repayment_acc_currency : Optional[str] = None
    interest_type : Optional[str] = None
    interest_rate_type: Optional[str] = None
    margin : Optional[str] = None
    interest_paid_by : Optional[str] = None


    def __post_init__(self):
        if self.type == ModelType.FINANCING.value:    
            self.create_finance()
        elif self.type == ModelType.REPAYMENT.value:
            self.repayment()


    def calculated_interest_amount(self):
        interest_rate = self.margin if self.interest_type == "FIXED" else 90 + self.margin
        current_date = date.today()
        calculated_date = (
            dt.strptime(str(self.due_date), "%Y-%m-%d")
            - dt.strptime(str(current_date), "%Y-%m-%d")
        ).days
        interest_amount = (self.finance_amount * interest_rate) * (calculated_date / 365)
        return interest_amount, interest_rate
        

    def create_finance(self):
        current_interest_amount = self.calculated_interest_amount()
        calculated_amount = self.finance_amount - current_interest_amount[0]
        exchange_rate_queryset = Exchangerate.objects.get(rate_currency=self.finance_currency)
        if self.program_type == ProgramType.APF.value:
            Finance.objects.create(
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


            if self.interest_paid_by == Partytype.ownparty.value:

                FinanceAccounting.objects.bulk_create([
                
                # type DEBIT 
                FinanceAccounting(contract_ref = self.finance_req_id, stage = ModelType.FINANCING.value ,
                type =  Accounttype.DEBIT.value , currency=self.finance_currency,amount = self.finance_amount , account = self.account_data_1 , 
                account_type= CustomerType.customer.value,base_currency= self.base_currency ,
                base_currency_amount= self.finance_amount * exchange_rate_queryset.rate_mid,
                exch_rate = exchange_rate_queryset.rate_mid),

                # type CREDIT
                FinanceAccounting(contract_ref = self.finance_req_id, stage = ModelType.FINANCING.value,
                type = Accounttype.CREDIT.value , currency=self.finance_currency,amount= self.finance_amount, account = self.account_data_2 , 
                account_type= CustomerType.customer.value,base_currency= self.base_currency ,
                base_currency_amount= self.finance_amount * exchange_rate_queryset.rate_mid,
                exch_rate = exchange_rate_queryset.rate_mid),
                
                ])

            if interest_paid_by == Partytype.counterparty.value:
                
                FinanceAccounting.objects.bulk_create([
                
                # type DEBIT 
                FinanceAccounting(contract_ref = self.finance_req_id, stage = ModelType.FINANCING.value , 
                type =  Accounttype.DEBIT.value  , currency=self.finance_currency,amount=self.finance_amount , account = self.account_data_1 , 
                account_type= CustomerType.customer.value,base_currency= self.base_currency,
                base_currency_amount= self.finance_amount * exchange_rate_queryset.rate_mid,
                exch_rate = exchange_rate_queryset.rate_mid),

                # type CREDIT
                FinanceAccounting(contract_ref = self.finance_req_id, stage = ModelType.FINANCING.value,
                type =  Accounttype.CREDIT.value  , currency=self.finance_currency,amount= calculated_amount, account = self.account_data_2 , 
                account_type= CustomerType.customer.value,base_currency= self.base_currency,
                base_currency_amount= calculated_amount * exchange_rate_queryset.rate_mid,
                exch_rate = exchange_rate_queryset.rate_mid),
                
                ])

            return current_interest_amount
        else:
            raise ValueError("program type should be APF , RF or DF")

    def repayment(self):

        Finance.objects.update_or_create(
                finance_id = self.finance_req_id,
                finance_request_id = self.finance_req_id,
                defaults={
                    "repayment_acc_currency" : self.repayment_acc_currency,
                    "repayment_account": self.repayment_account,
                    "status": ModelType.REPAYMENT.value
                }
            )
        # Finance.objects.update_or_create(
        #         finance_id = self.finance_req_id,
        #         finance_request_id = self.finance_req_id,
        #         defaults={
        #             "finance_date": self.due_date,
        #             "due_date": self.due_date,
        #             "invoice_currency": self.invoice_currency,
        #             "invoice_amount": self.invoice_amount,
        #             "finance_currency": self.finance_currency,
        #             "finance_amount": self.finance_amount,
        #             "settlement_currency": self.settlement_currency,
        #             "repayment_acc_currency" : self.repayment_acc_currency,
        #             "repayment_account": self.repayment_account,
        #             "interest_type": self.interest_type,
        #             "interest_rate_type": self.interest_rate_type,
        #             "margin": self.margin,
        #             "interest_paid_by": self.interest_paid_by,
        #             "own_party_account_info": self.own_party_account_info,
        #             "remittance_info":  self.remittance_info,
        #             "status": ModelType.REPAYMENT.value
        #         }
        #     )