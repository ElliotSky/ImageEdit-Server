from django.db import models

# Create your models here.

class AidrawDB(models.Model):
    '''
        image_index：图片索引（存储图片名）
        image_path：图片路径
        prompt_text：提示语
        prompt：提示词
        boxes：检测框
    '''
    image_index = models.CharField(max_length=255, blank=False, default='notindex')
    image_path = models.CharField(max_length=255, blank=False, default='notpath')
    prompt_text = models.CharField(max_length=255, blank=True, default='')
    prompt = models.CharField(max_length=255, blank=True, default='')
    boxes = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Image: {self.image_index}"

    class Meta:
        db_table = 'aidrawbd'
        verbose_name = 'AI Image'
        verbose_name_plural = 'AI Images'