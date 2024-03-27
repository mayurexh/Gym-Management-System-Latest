from django.shortcuts import render,redirect
from . import models
from . import forms
import stripe
from django.template.loader import get_template
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Count
from datetime import timedelta

def home(request):
    banners = models.Banners.objects.all()
    services = models.Service.objects.all()[:3]
    gimgs = models.GalleryImage.objects.all().order_by('-id')[:9]
    return render(request, 'main/home.html', {'banners': banners, 'services': services,
                                              'gimgs': gimgs})


def page_detail(request,id):
    page = models.Page.objects.get(id=id)
    return render(request, 'main/page.html', {'page': page})

def faq_list(request):
    faq = models.faq.objects.all()
    return render(request, 'main/faq.html', {'faq': faq})

def enquiry(request):
    msg = ''
    if request.method == "POST":
        form = forms.EnquiryForm(request.POST)
        if form.is_valid:
            form.save()
            msg = "Data is saved"
    form = forms.EnquiryForm
    return render(request, 'main/enquiry.html', {"form": form, "msg": msg})


def showGallery(request):
    gallerys = models.Gallery.objects.all().order_by('-id')
    return render(request, 'main/gallery.html',{'gallerys': gallerys})


#show gallery photos
def gallery_detail(request,id):
    gallery = models.Gallery.objects.get(id=id)
    gallery_imgs = models.GalleryImage.objects.filter(gallery=gallery).order_by('-id')
    return render(request, 'main/gallery_imgs.html',{'gallery_imgs' :gallery_imgs,
                                                     'gallery':gallery})


#show pricing
def pricing(request):
    plans = models.SubPlan.objects.annotate(total_members = Count('subscription__id')).all().order_by('id')
    dfeature = models.SubPlanFeature.objects.all()
    return render(request, 'main/pricing.html', {'plans': plans,
                                                 'dfeature' : dfeature})

#signup
def signup(request):
    msg = None
    if request.method == "POST":
        form = forms.SignUp(request.POST)
        if form.is_valid():
            form.save()
            msg = "Thankyou for registering"

    form = forms.SignUp
    return render(request, 'registration/signup.html', {'form': form,
                                                        'msg':msg} )


#checkout
def checkout(request,plan_id):
    planDetail = models.SubPlan.objects.get(pk = plan_id)
    return render(request, 'main/checkout.html', {'plan': planDetail})


#stripe key
stripe.api_key = "sk_test_51NwLUESDysNFZsyaC2WMc2eEnnRAX9QxRR3oel0JxHaHuYZdfYCLVL7lODQ3bTLNI6B8xPH5Z2lSerjMFx1fOQhM00erEVGphO"

def checkout_session(request, plan_id):
    plan = models.SubPlan.objects.get(pk= plan_id)
    session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items=[
                {
                    'price_data':{
                        'currency': 'inr',
                        'product_data':{
                            'name': plan.title
                        },
                        'unit_amount':plan.price
                    },
                    'quantity': 1
                },
            ],
            mode='payment', 
            success_url= 'http://127.0.0.1.8000/pay_success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://127.0.0.1.8000/pay_cancel',
            client_reference_id=plan_id
    )

    return redirect(session.url , code=303)

#success
from django.core.mail import EmailMessage

def pay_success(request):
    session =  stripe.checkout.Session.retrieve(request.GET['session_id'])
    plan_id = session.client_reference_id
    plan = models.SubPlan.objects.get(pk = plan_id)
    user = request.user
    models.Subscription.objects.ccreate(
        plan = plan,
        user = user,
        price = plan.price
    )
    subject = 'Order Email'
    html_content = get_template('main/orderemail.html').render({'title': plan.title})
    from_email = 'mayureshpisat18@gmail.com'
    msg = EmailMessage(subject, html_content, from_email, ['john@gmail.com'])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    return render(request, 'main/success.html')



#cancel
def pay_cancel(request):
    return render(request, 'main/cancel.html')

# User Dashboard Section Start
def user_dashboard(request):
    current_plan = models.Subscription.objects.get(user = request.user)
    my_trainer = models.AssignSubscriber.objects.get(user = request.user)
    enddate = current_plan.reg_date+timedelta(current_plan.plan.validity_days)
    #notifications fetch
    data = models.Notify.objects.all().order_by('-id')
    notifStatus = False
    jsonData = []
    totalUnread = 0
    for d in data:
        try:
            notifStatusData = models.NotifUserStatus.objects.filter(user = request.user,notif = d)
            if notifStatusData:
                notifStatus = True
        except models.NotifUserStatus.DoesNotExist:
            notifStatus = False
        if not notifStatus:
            totalUnread+=1
    return render(request, 'user/dashboard.html',{'current_plan': current_plan, 'my_trainer': my_trainer,
                                                  'totalUnread':totalUnread,
                                                  'enddate':enddate})


#edit form
def update_profile(request):
    msg = ""
    if request.method == "POST":
        form = forms.ProfileForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            msg = "Data is saved"
    else:
        form = forms.ProfileForm(instance = request.user)
    return render(request,'user/update-profile.html', {'form':form,
                                                       'msg':msg})

#trainer form view

def trainerlogin(request):
    msg = ''
    if request.method == "POST":
        username = request.POST["username"]
        pwd = request.POST["pwd"]
        trainer = models.Trainer.objects.filter(username = username, pwd = pwd).count()
        if trainer > 0:
            trainer = models.Trainer.objects.filter(username = username, pwd = pwd).first()
            request.session["trainerLogin"] = True
            request.session["trainerid"] = trainer.id
            return redirect("/trainer_dashboard")            
        else:
            msg = "Invalid"
    form = forms.TrainerLoginForm()
    return render(request, 'trainer/trainerlogin.html', {"form": form, "msg": msg})

def trainer_dashboard(request):
    return render(request, 'trainer/dashboard.html')

def trainer_profile(request):
    msg = ""
    if request.method == "POST":
        t_id = request.session["trainerid"] 
        trainer = models.Trainer.objects.get(id = t_id)
        form = forms.TrainerProfileForm( request.POST,request.FILES,instance=trainer)
        if form.is_valid():
            form.save()
        msg+="Profile Update Succesfully"
    
    t_id = request.session["trainerid"] 
    trainer = models.Trainer.objects.get(id = t_id)
    form = forms.TrainerProfileForm(instance=trainer)
    return render(request, 'trainer/profile.html', {'form':form,
                                                    'msg':msg})

def trainer_subscribers(request):
    trainer = models.Trainer.objects.get(pk = request.session["trainerid"])
    trainer_subs = models.AssignSubscriber.objects.filter(trainer = trainer).order_by('-id')
    return render(request, 'trainer/trainer_subscribers.html',{'trainer_subs': trainer_subs})

def trainer_payments(request):
    trainer = models.Trainer.objects.get(pk = request.session["trainerid"])
    trainer_pays = models.TrainerSalary.objects.filter(trainer = trainer).order_by('-id')
    return render(request, 'trainer/trainer_payments.html', {'trainer_pays':trainer_pays})

def trainer_changepassword(request):
    msg = " "
    if request.method == "POST":
        trainer = models.Trainer.objects.get(pk = request.session["trainerid"])
        old_password = request.POST["old_password"]
        new_password = request.POST["new_password"]
        #check old password
        if old_password == trainer.pwd:
            trainer.pwd = new_password
            trainer.save()
            msg+="Password changed successfully"
            del request.session["trainerLogin"]
            return redirect('/trainerlogin')
        else:
            msg += "Your old password is incorrect"
        form = forms.TrainerChangePassword(request.POST)
    form = forms.TrainerChangePassword
    return render(request, "trainer/trainer_changepassword.html",{'form':form,'msg':msg})

def trainerlogout(request):
    del request.session["trainerLogin"]
    return redirect('/trainerlogin')


def notifications(request):
    data = models.Notify.objects.all().order_by('-id')
    return render(request, 'main/notifs.html', {'data':data})


# #get all notifis
# def notifications(request):
#     data = models.Notify.objects.all().order_by('-id')
#     jsonData = serializers.serialize('json', data)
#     return JsonResponse({'data':jsonData})

# Get All Notifications
def get_notifs(request):
    data = models.Notify.objects.all().order_by('-id')
    notifStatus = False
    jsonData = []
    totalUnread = 0
    for d in data:
        try:
            notifStatusData = models.NotifUserStatus.objects.filter(user = request.user,notif = d)
            if notifStatusData:
                notifStatus = True
        except models.NotifUserStatus.DoesNotExist:
            notifStatus = False
        if not notifStatus:
            totalUnread+=1
        jsonData.append({
            'pk':d.id,
            'notify_detail':d.notify_detail,
            'notifStatus':notifStatus
        })
    return JsonResponse({'data':jsonData, 'totalUnread': totalUnread})

def mark_read_notif(request):
    notif=request.GET['notif']
    notif=models.Notify.objects.get(pk=notif)
    user=request.user
    models.NotifUserStatus.objects.create(notif=notif,user=user,status=True)
    return JsonResponse({'bool':True})

#Trainer_notifications
def trainer_notifs(request):
    data = models.TrainerNotification.objects.all().order_by('-id')
    return render(request, 'trainer/notifs.html', {'data':data})

# Trainer Messages
def trainer_msgs(request):
	data=models.TrainerMsg.objects.all().order_by('-id')
	return render(request, 'trainer/msgs.html',{'msgs':data})

#report for user
def report_for_user(request):
	trainer=models.Trainer.objects.get(id=request.session['trainerid'])
	msg=''
	if request.method=='POST':
		form=forms.ReportForUserForm(request.POST)
		if form.is_valid():
			new_form=form.save(commit=False)
			new_form.report_from_trainer=trainer
			new_form.save()
			msg='Data has been saved'
		else:
			msg='Invalid Response!!'
	form=forms.ReportForUserForm
	return render(request, 'main/report_for_user.html',{'form':form,'msg':msg})

#report for trainer
def report_for_trainer(request):
	user=request.user
	msg=''
	if request.method=='POST':
		form=forms.ReportForTrainerForm(request.POST)
		if form.is_valid():
			new_form=form.save(commit=False)
			new_form.report_from_user=user
			new_form.save()
			msg='Data has been saved'
		else:
			msg='Invalid Response!!'
	form=forms.ReportForTrainerForm
	return render(request, 'main/report_for_trainer.html',{'form':form,'msg':msg})


def contact(request):
    return render(request, 'main/contact_us.html')