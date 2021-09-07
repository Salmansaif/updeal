from django.contrib.auth.models import User
from django.db import models


from deals.models import Deal

STATUS_EXPIRED = 0
STATUS_ONHOLD = 1
STATUS_ACTIVE = 2
STATUS_REDEEMED = 3

STATUS = (
  # (STATUS_ONHOLD, "Purchased - ON HOLD"),
  (STATUS_ACTIVE, "Purchased - Money Collected"),
  (STATUS_REDEEMED, "Redeemed"),
  (STATUS_EXPIRED, "Expired"),
)


class Coupon(models.Model):
	user                    = models.ForeignKey(User, on_delete=models.CASCADE)
	deal                    = models.ForeignKey(Deal, on_delete=models.CASCADE) #coupon will be deleted if deal is deleted?
	status                  = models.IntegerField(choices=STATUS, default=0)
	entry_date              = models.DateTimeField(blank=True, editable=False, null=True, auto_now_add=True)
	last_mod                = models.DateTimeField(blank=True, editable=False, null=True, auto_now=True)
	deleted_date            = models.DateTimeField(blank=True, editable=False, null=True)
	#qr_code_data
	
	class Meta:
		verbose_name = 'Coupon'
		verbose_name_plural = 'Coupons'
	
	def __str__(self):
		return str(self.user)