from django.contrib import admin
from . import models
import stripe


class BannerAdmin(admin.ModelAdmin):
    list_display=('alt_text','image_tag')
admin.site.register(models.Banners,BannerAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display=('title','image_tag')
admin.site.register(models.Service,ServiceAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display=('title',)
admin.site.register(models.Page)

class faqAdmin(admin.ModelAdmin):
    list_display=('quest',)
admin.site.register(models.faq)

class EnquiryAdmin(admin.ModelAdmin):
    list_display= ('full_name','email','details', 'send_time')
admin.site.register(models.Enquiry, EnquiryAdmin)


class GalleryAdmin(admin.ModelAdmin):
    list_display=('title', 'image_tag')
admin.site.register(models.Gallery,GalleryAdmin)

class GalleryImageAdmin(admin.ModelAdmin):
    list_display=('alt_text', 'image_tag')

admin.site.register(models.GalleryImage,GalleryImageAdmin)


#subplan admin
class SubPlanAdmin(admin.ModelAdmin):
    list_editable = ('highlight_status','max_member')
    list_display= ('title', 'price','highlight_status','max_member','validity_days')
admin.site.register(models.SubPlan, SubPlanAdmin)

#subplan features admin
class SubPlanFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'subplans', )
    def subplans(self,obj):
        return " | ".join([sub.title for sub in obj.subplan.all()])
admin.site.register(models.SubPlanFeature, SubPlanFeatureAdmin)

#discount 
class PlanDiscountAdmin(admin.ModelAdmin):
    list_display = ('total_months', 'total_discount',)
admin.site.register(models.PlanDiscount, PlanDiscountAdmin)


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('user', 'image_tag','mobile',)
admin.site.register(models.Subscriber, SubscriberAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user','plan', 'price', "reg_date",)
admin.site.register(models.Subscription, SubscriptionAdmin)


class TrainerAdmin(admin.ModelAdmin):
    list_editable = ('is_active',)
    list_display = ('full_name','mobile', 'address', 'is_active','img', 'salary' )
admin.site.register(models.Trainer, TrainerAdmin)


class NotifyAdmin(admin.ModelAdmin):
    list_display = ('notify_detail','read_by_user', 'read_by_trainer', )
admin.site.register(models.Notify, NotifyAdmin)

class NotifyUserStatusAdmin(admin.ModelAdmin):
    list_display = ('notif','user','status')
admin.site.register(models.NotifUserStatus, NotifyUserStatusAdmin)


class AssignSubscriberAdmin(admin.ModelAdmin):
    list_display = ('user','trainer', )
admin.site.register(models.AssignSubscriber, AssignSubscriberAdmin)


class TrainerSalaryAdmin(admin.ModelAdmin):
	list_display=('trainer','amt','amt_date')
admin.site.register(models.TrainerSalary,TrainerSalaryAdmin)

class TrainerNotificationAdmin(admin.ModelAdmin):
    list_display = ('notif_msg',)
admin.site.register(models.TrainerNotification, TrainerNotificationAdmin)

class TrainerMsgAdmin(admin.ModelAdmin):
    list_display = ('user','trainer','messages',)
admin.site.register(models.TrainerMsg, TrainerMsgAdmin)

class TrainerSubscriberReportAdmin(admin.ModelAdmin):
	list_display=('report_msg','report_for_trainer','report_for_user','report_from_trainer','report_from_user')
admin.site.register(models.TrainerSubscriberReport,TrainerSubscriberReportAdmin)



class AppSettingAdmin(admin.ModelAdmin):
	list_display=('image_tag',)
admin.site.register(models.AppSetting,AppSettingAdmin)
# Register your models here.

