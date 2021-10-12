from django.db import models
from django.contrib.auth.models import User , Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _




# Create your models here.






# class Status(models.Model):
#     phase = models.CharField(max_length= 200)
#     def __str__(self):
#         return self.phase

class LoanFund(models.Model):

    class Status(models.TextChoices):
        NO_APPLICANTS = 'NA' , _('No Applicants')
        IN_PROCESS = 'IP' , _('In Process')
        APPROVED = 'AP' , _('Approved')
        DENIED = 'DN' , _('Denied')
    
    def allowedDefault():
         #return {"name": "bankPersonnel"}
         return Group.objects.get(name = 'bankPersonnel')

    amount = models.PositiveIntegerField(null = True, blank = True)
    allowed = models.ManyToManyField(Group)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.NO_APPLICANTS,
    )
    #status = models.ForeignKey(Status,on_delete=models.CASCADE, null = True, default= 1)
    creator = models.ForeignKey(User,on_delete = models.CASCADE , null = True, blank = True)
    provider = models.ForeignKey(User,on_delete= models.CASCADE,related_name='provider', null = True, blank= True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    fund_type = models.CharField(max_length=200)
    duration_years = models.PositiveIntegerField()
    intrest_rate = models.FloatField()
    max_amount = models.PositiveIntegerField()
    min_amount = models.PositiveIntegerField()





class LoanTerm(models.Model):
    class Status(models.TextChoices):
        NO_APPLICANTS = 'NA' , _('No Applicants')
        IN_PROCESS = 'IP' , _('In Process')
        APPROVED = 'AP' , _('Approved')
        DENIED = 'DN' , _('Denied')
    
    def allowedDefault():
         #return {"name": "bankPersonnel"}
         return Group.objects.get(name = 'bankPersonnel')


    amount = models.PositiveIntegerField(null = True, blank = True)
    allowed = models.ManyToManyField(Group)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.NO_APPLICANTS,
    )
  #  status = models.ForeignKey(Status,on_delete = models.CASCADE,null = True, default = 1)
    creator = models.ForeignKey(User,on_delete = models.CASCADE , null = True, blank = True)
    customer = models.ForeignKey(User,on_delete= models.CASCADE,related_name='customer', null = True, blank = True) 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    loan_type = models.CharField(max_length=200)
    duration_years = models.PositiveIntegerField()
    intrest_rate = models.FloatField()
    max_amount = models.PositiveIntegerField()
    min_amount = models.PositiveIntegerField()

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     funds = models.ManyToManyField(LoanFund)
#     loans = models.ManyToManyField(LoanTerm)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()    
