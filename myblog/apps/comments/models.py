from django.db import models

# Create your models here.
class Comments(models.Model):
    com_id = models.AutoField(primary_key=True, verbose_name="评论id")
    com_content = models.CharField(max_length=500,verbose_name="评论内容")
    createtime = models.DateTimeField(auto_now_add=True,verbose_name="评论时间")
    username = models.CharField(max_length=20,verbose_name="用户名称")
    blog_id = models.IntegerField(verbose_name="博客id")
    
    class Meta:
        db_table = "comments"
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return self.com_id