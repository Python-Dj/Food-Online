from django.db import models
from accounts.models import User, UserProfile

from accounts.utils import send_notification


class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='user_profile')
    vendor_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    vendor_license = models.ImageField(upload_to="vender/license")
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    

    def save(self, *args, **kwargs):
        if self.pk is not None:
            mail_template = "accounts/emails/admin_approval_email.html"
            context = {
                "user": self.user,
                "is_approved": self.is_approved,
            }
            if self.is_approved == True:
                # send email notification.
                mail_subject = "Congratulations! Your resturant has benn approved."
                send_notification(mail_subject, mail_template, context)
            else:
                #send email notification.
                mail_subject = "You are not eligible for publishing your food menu on our marketplace."
                send_notification(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args, **kwargs)
