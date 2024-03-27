from django.db import models
from django.utils.html import mark_safe
from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#Banners

class Banners(models.Model):
    img = models.ImageField(upload_to='banners/')
    alt_text = models.CharField(max_length = 150)
    
    def __str__(self) -> str:
        return self.alt_text
    def image_tag(self):
        return mark_safe('<img src="%s" width="80"/>'  % (self.img.url))
    

class Service(models.Model):
    title = models.CharField(max_length=150)
    detail = models.TextField()
    img = models.ImageField(upload_to="services/", null=True)

    def __str__(self) -> str:
        return self.title
    def image_tag(self):
        return mark_safe('<img src="%s" width="80"/>'  % (self.img.url))

    
#Pages model
    
class Page(models.Model):
    title= models.CharField(max_length=200)
    details = models.TextField()

    def __str__(self) -> str:
        return self.title

#FAQ model

class faq(models.Model):
    quest= models.TextField()
    ans = models.TextField()

    def __str__(self) -> str:
        return self.quest
    
#enquiry model

class Enquiry(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    details = models.TextField()
    send_time = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.full_name

#gallery model
class Gallery(models.Model):
    title = models.CharField(max_length=150)
    detail = models.TextField()
    img = models.ImageField(upload_to="gallery/", null=True)
    def __str__(self) -> str:
        return self.title
    def image_tag(self):
        return mark_safe('<img src="%s" width="80"/>'  % (self.img.url))

class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete = models.CASCADE,null=True)
    alt_text = models.CharField(max_length=150)
    detail = models.TextField()
    img = models.ImageField(upload_to="gallery_imgs/", null=True)
    def __str__(self) -> str:
        return self.alt_text
    def image_tag(self):
        return mark_safe('<img src="%s" width="80"/>'  % (self.img.url))
    
#subscription plan
class SubPlan(models.Model):
    title = models.CharField(max_length = 150)
    price = models.CharField(max_length = 50)
    max_member = models.IntegerField(null = True)
    highlight_status = models.BooleanField(default = False, null = True)
    validity_days = models.IntegerField(null = True)
    def __str__(self) -> str:
        return self.title
    
#subscrption plan feature
class SubPlanFeature(models.Model):
    # subplan = models.ForeignKey(SubPlan, on_delete = models.CASCADE)
    subplan = models.ManyToManyField(SubPlan)
    title = models.CharField(max_length = 150)

    
    def __str__(self) -> str:
        return self.title


#discount model
class PlanDiscount(models.Model):
    subplan = models.ForeignKey(SubPlan, on_delete =models.CASCADE, null = True)
    total_months = models.IntegerField()
    total_discount = models.IntegerField()

    def __str__(self) -> str:
        return str(self.total_months)
    
#subscriber model

class Subscriber(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,null = True)
    mobile = models.CharField(max_length = 20)
    address = models.TextField()
    img = models.ImageField(upload_to="subs/")

    # def __str__(self) -> str:
    #     return self.user

    def image_tag(self):
        if self.img:
            return mark_safe('<img src="%s" width="80"/>'  % (self.img.url))
        else:
            return 'no-image'



@receiver(post_save,sender=User)
def create_subscriber(sender,instance, created,**kwargs):
    if created:
        Subscriber.objects.create(user=instance)
    


#subscription model
    
    
class Subscription(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,null = True)
    plan = models.ForeignKey(SubPlan,on_delete = models.CASCADE,null = True)
    price = models.IntegerField()
    reg_date = models.DateField(auto_now_add = True, null = True)

   
#trainer model
class Trainer(models.Model):
    full_name = models.CharField(max_length = 100)
    username = models.CharField(max_length = 100, null = True)
    pwd = models.CharField(max_length = 100, null = True)
    mobile = models.CharField(max_length = 100)
    address = models.TextField()
    is_active = models.BooleanField(default = False)
    details = models.TextField()
    img = models.ImageField(upload_to="trainers/")
    instagram = models.CharField(max_length = 100, null = True)
    facebook = models.CharField(max_length = 100, null = True)
    salary = models.IntegerField(null = True)
    

    def __str__(self) -> str:
        return self.full_name
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="80"/>'  % (self.img.url))
    

#notification

class Notify(models.Model):
    notify_detail = models.TextField()
    read_by_user = models.ForeignKey(User,on_delete = models.CASCADE, null = True, blank = True)
    read_by_trainer = models.ForeignKey(Trainer,on_delete = models.CASCADE, null = True, blank = True)

    
    def __str__(self) -> str:
        return self.notify_detail

#Mark as read notification by User
    
class NotifUserStatus(models.Model):
    notif = models.ForeignKey(Notify, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    status = models.BooleanField(default = False)


class AssignSubscriber(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	trainer=models.ForeignKey(Trainer, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.subscriber)


class TrainerSalary(models.Model):
	trainer=models.ForeignKey(Trainer, on_delete=models.CASCADE)
	amt=models.IntegerField()
	amt_date=models.DateField()
	remarks=models.TextField(blank=True)

	class Meta:
		verbose_name_plural='Trainer Salary'

	def __str__(self):
		return str(self.trainer.full_name)
    
class TrainerNotification(models.Model):
    notif_msg = models.TextField()
    def __str__(self) -> str:
        return self.notif_msg
    
class NotifTrainerStatus(models.Model):
    notif = models.ForeignKey(TrainerNotification, on_delete = models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete = models.CASCADE)
    status = models.BooleanField(default = False)

#Subscriber msg for trainer model
class TrainerMsg(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    trainer=models.ForeignKey(Trainer, on_delete=models.CASCADE)
    messages = models.TextField()
    class Meta:
        verbose_name_plural = "msg for trainers"

class TrainerSubscriberReport(models.Model):
    report_for_user=models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name = "report_for_user")
    report_for_trainer=models.ForeignKey(Trainer, on_delete=models.CASCADE, null = True, related_name = "report_for_trainer")
    report_from_user=models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name = "report_from_user")
    report_from_trainer=models.ForeignKey(Trainer, on_delete=models.CASCADE, null = True, related_name = "report_from_trainer")
    report_msg = models.TextField()
    

class AppSetting(models.Model):
	logo_img=models.ImageField(upload_to='app_logos/')

	def image_tag(self):
		return mark_safe('<img src="%s" width="80" />' % (self.logo_img.url))