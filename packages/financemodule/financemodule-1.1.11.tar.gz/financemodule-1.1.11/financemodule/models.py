from django.db import models




class Finance(models.Model):
    finance_id = models.CharField(max_length=55)
    finance_date = models.DateField()
    finance_request_id = models.IntegerField()
    program_type = models.CharField(max_length=55)
    anchor_party = models.IntegerField()
    counterparty = models.IntegerField()
    due_date = models.DateField()
    invoice_currency = models.CharField(max_length=55)
    invoice_amount = models.IntegerField()
    finance_currency = models.CharField(max_length=55)
    finance_amount = models.IntegerField()
    settlement_currency = models.CharField(max_length=55)
    settlement_amount = models.IntegerField()
    repayment_acc_currency = models.CharField(max_length=55)
    repayment_account = models.CharField(max_length=55)
    interest_type = models.CharField(max_length=55)
    interest_rate_type = models.CharField(max_length=55)
    margin = models.FloatField()
    interest_rate = models.FloatField()
    interest_amount = models.IntegerField()
    interest_paid_by = models.CharField(max_length=55)
    own_party_account_info = models.CharField(max_length=55)
    remittance_info = models.CharField(max_length=55)
    status = models.CharField(max_length=55)
    created_date = models.DateTimeField(auto_now_add=True)


class FinanceAccounting(models.Model):
    contract_ref = models.CharField(max_length=155,blank=True , null = True)
    stage = models.CharField(max_length=155,blank=True , null = True)
    type = models.CharField(max_length=155,blank=True , null = True)
    currency = models.CharField(max_length=155,blank=True , null = True)
    amount = models.IntegerField(blank=True , null = True)
    account = models.CharField(max_length=55,blank=True , null = True)
    account_type = models.CharField(max_length=155,blank=True , null = True)
    base_curreny = models.CharField(max_length=155,blank=True , null = True)
    base_currency_amount = models.IntegerField(blank=True , null = True)
    exch_rate = models.FloatField(blank=True , null = True)
    created_date = models.DateTimeField(auto_now_add=True)


class Exchangerate(models.Model):
    bank_entity = models.IntegerField(blank=True , null = True)
    rate_base_currency = models.CharField(max_length=255)
    rate_currency = models.CharField(max_length=255)
    rate_date = models.DateField()
    rate_previous_day = models.DateField()
    rate_buy = models.FloatField(blank=True , null = True)
    rate_sell = models.FloatField(blank=True , null = True)
    rate_mid = models.FloatField(blank=True , null = True)
    created_date = models.DateTimeField(auto_now_add=True)