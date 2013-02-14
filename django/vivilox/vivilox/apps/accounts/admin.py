from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from vivilox.apps.accounts.models import UserProfile
from django.contrib.admin import ModelAdmin


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = False
    verbose_name_plural = 'Profile'

# Define a new User admin
class UserAdmin(UserAdmin):
	inlines = (UserProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class UserProfileAdmin(admin.ModelAdmin):
	list_display       = ('fullname','user_username','user_type','email')
	list_display_links = ('fullname','user_username','email')
	list_filter        = ('user_type','user__is_active',)
	ordering           = ('user_type',)
	search_fields      = ('user__username','user__first_name','user__last_name',)
	
	def user_username(self,instance):
		return '<span style="bold:true">%s</span>' % (instance.user.username)
	user_username.short_description = "UserName"
	user_username.allow_tags = True
	
	def fullname(self,instance):
		_fullname =  "%s %s" % (instance.user.first_name,instance.user.last_name)
		if not _fullname.strip():
			return '<span style="color:red">Please fill empty fields in User Admin</span>'
		else:
			return _fullname
	fullname.short_description = "Name"
	fullname.allow_tags = True

	def email(self,instance):
		return instance.user.email
	email.short_description = "Email"

	def m_status(self,instance):
		return str(self.is_active)
	m_status.short_description = "Active"


#admin.site.register(UserProfile,UserProfileAdmin)