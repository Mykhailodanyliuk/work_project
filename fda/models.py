from django.db import models


class DeviceEvent(models.Model):
    generic_name = models.CharField(max_length=128)
    brand_name = models.CharField(max_length=128)
    udi_di = models.CharField(max_length=30)
    data = models.JSONField()
    upload_at = models.DateTimeField(auto_now=True)


class Device(models.Model):
    name = models.TextField()
    k_number = models.CharField(max_length=128)
    data_json = models.JSONField()
    upload_at = models.DateTimeField(auto_now=True)


class DeviceEnforcement(models.Model):
    event_id = models.CharField(max_length=128)
    recalling_firm = models.CharField(max_length=128)
    data = models.JSONField()
    upload_at = models.DateTimeField(auto_now=True)


class DeviceRecall(models.Model):
    cfres_id = models.CharField(max_length=128)
    res_event_number = models.CharField(max_length=128)
    recalling_firm = models.CharField(max_length=255)
    data = models.JSONField()
    upload_at = models.DateTimeField(auto_now=True)


class DeviceClassification(models.Model):
    device_name = models.CharField(max_length=255)
    medical_specialty_description = models.CharField(max_length=255)
    regulation_number = models.CharField(max_length=32)
    data = models.JSONField()
    upload_at = models.DateTimeField(auto_now=True)


class DeviceCovid19(models.Model):
    sample_id = models.CharField(max_length=16)
    lot_number = models.CharField(max_length=32)
    device = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    data = models.JSONField()
    upload_at = models.DateTimeField(auto_now=True)


class DevicePMA(models.Model):
    pma_number = models.CharField(max_length=16)
    supplement_number = models.CharField(max_length=16)
    applicant = models.CharField(max_length=255)
    trade_name = models.CharField(max_length=255)
    data = models.JSONField()
    upload_at = models.DateTimeField(auto_now=True)


class DeviceRegistrationListings(models.Model):
    registration_number = models.CharField(max_length=64)
    fei_number = models.CharField(max_length=64)
    name = models.CharField(max_length=255)
    data = models.JSONField()
    upload_at = models.DateTimeField(auto_now=True)


class DeviceUDI(models.Model):
    public_device_record_key = models.CharField(max_length=128)
    device_description = models.TextField()
    brand_name = models.CharField(max_length=255)
    data = models.JSONField()
    upload_at = models.DateTimeField(auto_now=True)


class DrugEnforcement(models.Model):
    event_id = models.CharField(max_length=64)
    recalling_firm = models.CharField(max_length=255)
    data = models.JSONField()
    upload_at = models.DateTimeField(auto_now=True)


class DrugEvent(models.Model):
    safety_report_id = models.CharField(max_length=64)
    company_numb = models.CharField(max_length=255)
    data = models.JSONField()
    upload_at = models.DateTimeField(auto_now=True)


class DrugNDC(models.Model):
    product_ndc = models.CharField(max_length=64)
    labeler_name = models.CharField(max_length=255)
    data = models.JSONField()
    upload_at = models.DateTimeField(auto_now=True)


class FoodEnforcement(models.Model):
    event_id = models.CharField(max_length=64)
    recalling_firm = models.CharField(max_length=255)
    data = models.JSONField()
    upload_at = models.DateTimeField(auto_now=True)


class FoodEvent(models.Model):
    report_number = models.CharField(max_length=64)
    data = models.JSONField()
    upload_at = models.DateTimeField(auto_now=True)
