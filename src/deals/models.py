from django.conf import settings
from django.db import models
from django.urls import reverse

User = settings.AUTH_USER_MODEL



PROVINCES = (
	('Sd', 'Sindh'),
	('Pj', 'Punjab'),
	('kpk', 'Khyber Pakhtun Khua'),
	('bn', 'Balochistan'),
)


class City(models.Model):
	"""
	City database (latitude, longitude, postalcode)
	"""
	name = models.CharField("City Name", max_length=60, unique=True)
	slug = models.SlugField(unique=True)
	is_active = models.BooleanField(default=False) #Are we operating in this city?
	province = models.CharField("Province", max_length=2, choices=PROVINCES)
	order = models.IntegerField(default = 0)

	class Meta:
		verbose_name = 'City'
		verbose_name_plural = 'Cities'

	def __str__(self):
		return self.name


class Advertiser(models.Model):
	user			= models.OneToOneField(User, on_delete=models.CASCADE)
	business_title 	= models.CharField(max_length=60)
	address 		= models.CharField(max_length=60)
	city 			= models.ForeignKey(City, on_delete=models.CASCADE)
	# postalcode 	= models.CharField(max_length=7)
	province 		= models.CharField(max_length=25, choices=PROVINCES)
	# country    	= models.ForeignKey(Country)
	cell 			= models.CharField(max_length=25)
	business_email 	= models.EmailField(blank=True, help_text="Email address of contact") #it should be removed from here
	
	def __str__(self):
		return self.business_title
	
	class Meta:
		verbose_name = 'Advertiser'
		verbose_name_plural = 'Advertisers'


class ProductCategory(models.Model):
	"""
	Categories for various products
	"""
	title 		= models.CharField("Category", max_length=60)
	slug 		= models.SlugField(unique=True)
	description = models.TextField(null=True, blank=True)
	active 		= models.BooleanField(default=True)
	
	class Meta:
		verbose_name = 'Product Category'
		verbose_name_plural = 'Product Categories'
		
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("category_detail", kwargs={"slug": self.slug})


class Deal(models.Model):
	"""
	Deal model
	"""
	title                   = models.CharField("Title", max_length=100)
	advertiser              = models.ForeignKey('Advertiser', on_delete=models.CASCADE, help_text="advertiser of the deal", verbose_name="Advertiser")
	city                    = models.ForeignKey(City, on_delete=models.CASCADE)
	slug                    = models.SlugField(unique=True)
	
	category                = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
	date_published          = models.DateTimeField()
	retail_price            = models.DecimalField(default=0, decimal_places=2, max_digits=6, help_text='Full retail price')
	deal_price              = models.DecimalField(default=0, decimal_places=2, max_digits=6, help_text='Deal (real) Price')
	bought					= models.IntegerField(default=0)
	
	discount_percentage     = models.DecimalField(default=0, decimal_places=2, max_digits=6, help_text='% Percentage Off retail')
	discount_value          = models.DecimalField(default=0, decimal_places=2, max_digits=6, help_text='$ Dollars Off retail')
	auction_duration        = models.IntegerField(default=24, help_text='Deal duration in hours')
	
	active             		= models.BooleanField(default=True)
	fine_print              = models.TextField(help_text="terms & conditions")
	tipping_point           = models.IntegerField(default=1, help_text='sales should reach for deal to valid')
	tipped_at               = models.DateTimeField(blank=True, null=True) #deal open for redeem time
	max_available           = models.IntegerField(default=0)
	description             = models.TextField(help_text="what you'll get")
	# reviews                 = models.TextField() #Need seperate model also for rating
	# address                 = models.TextField()
	# tags                    = TagField(help_text="Tags seperated by commas!!", verbose_name='tags')
	featured				= models.BooleanField(default=False)
	views					= models.IntegerField(help_text="views count for today")
	
	latitude                = models.DecimalField("Latitude (decimal)", max_digits=9, decimal_places=6, blank=True, null=True)
	longitude               = models.DecimalField("Longitude (decimal)", max_digits=9, decimal_places=6, blank=True, null=True)
	
	entry_date              = models.DateTimeField(blank=True, editable=False, null=True, auto_now_add=True)
	last_mod                = models.DateTimeField(blank=True, editable=False, null=True, auto_now=True)
	deleted_date            = models.DateTimeField(blank=True, editable=False, null=True)
	
	class Meta:
		verbose_name = 'Deal'
		verbose_name_plural = 'Deals'

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		# return "{slug}/".format(slug=self.slug)
		return reverse("deals:detail", kwargs={"slug": self.slug})

	def num_available(self):
		return self.max_available - self.num_sold()

	def num_sold(self):
		return self.coupon_set.count()

	def percentage_sold(self):
		num_sold = self.num_sold()
		if num_sold > self.tipping_point:
			return 100
		else:
			return int( ( (num_sold*1.0) / self.tipping_point) * 100)
		
	def num_needed(self):
		num_sold = self.num_sold()
		if num_sold > self.tipping_point:
			return 0
		else:
			return self.tipping_point - num_sold

