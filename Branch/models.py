from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Branch(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    address = models.CharField(max_length=128, verbose_name='العنوان', null=True, blank=True)
    phone = models.CharField(max_length=128, verbose_name='التليفون', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name="اضيف بواسطة", on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        default_permissions = ()
        permissions = (
            ('add_branch', 'إضافة فرع'),
            ('edit_branch', 'تعديل فرع'),
            ('delete_branch', 'حذف فرع'),
            ('access_branch_menu', 'الدخول علي قائمة الفروع'),
        )
