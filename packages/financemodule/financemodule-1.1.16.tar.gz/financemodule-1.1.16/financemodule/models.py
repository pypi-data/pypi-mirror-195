from django.db import models




class Finance(models.Model):
    finance_id = models.CharField(max_length=255,blank=True , null = True)
    finance_date = models.DateField(blank=True , null = True)
    finance_request_id = models.IntegerField(blank=True , null = True)
    program_type = models.CharField(max_length=255,blank=True , null = True)
    anchor_party = models.IntegerField(blank=True , null = True)
    counterparty = models.IntegerField(blank=True , null = True)
    due_date = models.DateField(blank=True, null=True)
    invoice_currency = models.CharField(max_length=255)
    invoice_amount = models.IntegerField(blank=True , null = True)
    finance_currency = models.CharField(max_length=255)
    finance_amount = models.IntegerField(blank=True , null = True)
    settlement_currency = models.CharField(max_length=255,blank=True , null = True)
    settlement_amount = models.IntegerField(blank=True , null = True)
    repayment_acc_currency = models.CharField(max_length=255)
    repayment_account = models.CharField(max_length=255)
    interest_type = models.CharField(max_length=255)
    interest_rate_type = models.CharField(max_length=255)
    margin = models.FloatField(blank=True , null = True)
    interest_rate = models.FloatField(blank=True , null = True)
    interest_amount = models.IntegerField(blank=True , null = True)
    interest_paid_by = models.CharField(max_length=255)
    own_party_account_info = models.CharField(max_length=255,blank=True , null = True)
    remittance_info = models.CharField(max_length=255,blank=True , null = True)
    status = models.CharField(max_length=255,blank=True , null = True)
    created_date = models.DateTimeField(auto_now_add=True)


class FinanceAccounting(models.Model):
    contract_ref = models.CharField(max_length=155,blank=True , null = True)
    stage = models.CharField(max_length=155,blank=True , null = True)
    type = models.CharField(max_length=155,blank=True , null = True)
    currency = models.CharField(max_length=155,blank=True , null = True)
    amount = models.IntegerField(blank=True , null = True)
    account = models.CharField(max_length=255,blank=True , null = True)
    account_type = models.CharField(max_length=155,blank=True , null = True)
    base_currency= base_currency = models.CharField(max_length=155,blank=True , null = True)
    base_currency_amount = models.IntegerField(blank=True , null = True)
    exch_rate = models.FloatField(blank=True , null = True)
    created_date = models.DateTimeField(auto_now_add=True)


class Exchangerate(models.Model):
    bank_entity = models.IntegerField(blank=True , null = True)
    rate_base_currency = models.CharField(max_length=255 , blank=True , null = True)
    rate_currency = models.CharField(max_length=255 , blank=True , null = True)
    rate_date = models.DateField(blank=True, null=True)
    rate_previous_day = models.DateField(blank=True, null=True)
    rate_buy = models.FloatField(blank=True , null = True)
    rate_sell = models.FloatField(blank=True , null = True)
    rate_mid = models.FloatField(blank=True , null = True)
    created_date = models.DateTimeField(auto_now_add=True)