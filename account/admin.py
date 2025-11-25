# from django.contrib import admin
# from django import forms
# from django.contrib.auth import get_user_model
# from django.utils.crypto import get_random_string

# User = get_user_model()

# class ShopAdminForm(forms.ModelForm):
#     # فیلدهایی که می‌خواهیم ادمین برای ساخت owner وارد کنه
#     owner_username = forms.CharField(required=False, label="Owner username")
#     owner_email = forms.EmailField(required=False, label="Owner email")
#     owner_password = forms.CharField(required=False, 
#                                     label="Owner password",
#                                     widget=forms.PasswordInput, 
#                                     help_text="اگر خالی بماند، پسورد خودکار ساخته می‌شود")


#     def clean(self):
#         cleaned = super().clean()
#         username = cleaned.get('owner_username')
#         password = cleaned.get('owner_password')
#         email = cleaned.get('owner_email')

#         # اگر ادمین فیلد username رو وارد کرده، مطمئن بشیم وجود نداره
#         if username:
#             if User.objects.filter(username=username).exists():
#                 raise forms.ValidationError("نام‌کاربری وارد شده قبلاً استفاده شده است.")
#         return cleaned

#     def save(self, commit=True):
#         shop = super().save(commit=False)
#         username = self.cleaned_data.get('owner_username')
#         email = self.cleaned_data.get('owner_email')
#         password = self.cleaned_data.get('owner_password')

#         if username:
#             # اگر پسورد ندادن، پسورد تصادفی بساز
#             if not password:
#                 password = get_random_string(8)  # می‌تونی طول رو تغییر بدی

#             user = User.objects.create(username=username, email=email)
#             user.set_password(password)
#             user.save()
#             shop.owner = user

#             # می‌تونیم این پسورد رو به ادمین برگردونیم یا ایمیل بزنیم
#             # برای سادگی، آن را در آبجکت shop._owner_plain_password نگه می‌داریم
#             shop._owner_plain_password = password

#         if commit:
#             shop.save()
#         return shop

#     def save_model(self, request, obj, form, change):
#         super().save_model(request, obj, form, change)
#         pwd = getattr(obj, '_owner_plain_password', None)
#         if pwd:
#             self.message_user(request, f"کاربر صاحب شاپ ساخته شد. نام‌کاربری: {obj.owner.username} - رمز: {pwd}")



# @admin.register(Shop)
# class ShopAdmin(admin.ModelAdmin):
#     form = ShopAdminForm
#     list_display = ('name', 'owner', 'phone', 'created_at')

