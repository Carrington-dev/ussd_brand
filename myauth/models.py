from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from myauth.countries import OCCUPATION, countries



"""MODEL MANAGER"""
class NewUserManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_active = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class NewUser(AbstractBaseUser):
	country 				= models.CharField(max_length=200, verbose_name="country", choices=countries, default="ZA")
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= models.CharField(max_length=30, verbose_name="username", unique=True)
	first_name          	= models.CharField(max_length=30,verbose_name="first name",  unique=False)
	last_name 				= models.CharField(max_length=30,verbose_name="last name",  unique=False)
	phone   				= models.CharField(max_length=30, verbose_name="phone", unique=False)
	disability 				= models.CharField(max_length=30, verbose_name="disability", unique=False)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False, verbose_name="admin",)
	is_active				= models.BooleanField(default=True, verbose_name="active",)
	is_verified				= models.BooleanField(default=False, verbose_name="verified",)
	is_staff				= models.BooleanField(default=False, verbose_name="staff",)
	is_superuser			= models.BooleanField(default=False, verbose_name="superuser",)
	is_teacher			    = models.BooleanField(default=False, verbose_name="teacher",)
	is_student			    = models.BooleanField(default=True, verbose_name="student",)
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']
	
	objects = NewUserManager()
	
	def __str__(self):
		return self.email 	# For checking permissions. to keep it simple all admin have ALL permissons
	
	def has_perm(self, perm, obj=None):
		return self.is_admin 	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
		
	def has_module_perms(self, app_label):
		return True

	class Meta:
		verbose_name = "User"
		verbose_name_plural = "Users"


class Profile(models.Model):
	user = models.OneToOneField(NewUser, verbose_name="user", on_delete=models.CASCADE)
	occupation = models.CharField(max_length=400, choices=OCCUPATION, default='Student')
	facebook_link = models.CharField(max_length=400, default='https://stemgon.co.za/')
	instagram_link = models.CharField(max_length=400, default='https://stemgon.co.za/')
	twitter_link = models.CharField(max_length=400, default='https://stemgon.co.za/')
	linkedin_link = models.CharField(max_length=400, default='https://stemgon.co.za/')
	specialty = models.CharField(max_length=400,  default='Mathematics')
	bio = models.TextField(blank=True, null=True)


	def __str__(self):
		return f"{self.user.username}'s Profile"


	@receiver(post_save, sender=NewUser)
	def create_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)


	@receiver(post_save, sender=NewUser)
	def save_profile(sender, instance, **kwargs):
		instance.profile.save()

	class Meta:
		verbose_name = "Profile"
		verbose_name_plural = "Profiles"