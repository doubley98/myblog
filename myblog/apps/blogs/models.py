from django.db import models


# Create your models here.
class Blogs(models.Model):
    blog_id = models.AutoField(primary_key=True, verbose_name="博客id")
    blog_title = models.CharField(max_length=50, verbose_name="博客标题")
    author = models.CharField(max_length=20, verbose_name="作者")
    content = models.TextField(max_length=5000, verbose_name="博客内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "blogs"
        verbose_name = "博客"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.blog_title
