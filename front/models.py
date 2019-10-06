from django.db import models


# Create your models here.
class UploadImages(models.Model):
    image = models.ImageField(upload_to='image', default='media/image/default.png',
                              max_length=100, verbose_name='图像', blank=True, null=True)
    image_processed = models.ImageField(upload_to='image_processed', default='media/image/default.png',
                                        max_length=100, verbose_name='图像1', blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fogy'


class SeamCarvingPicture(models.Model):
    image = models.ImageField(upload_to='image', default='media/image/default.png',
                              max_length=100, verbose_name='图像', blank=True, null=True)
    image_processed = models.ImageField(upload_to='image/image_processed', default='media/image/default.png',
                                        max_length=100, verbose_name='图像1', blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'SeamCarving'


class sift(models.Model):
    image1 = models.ImageField(upload_to='image', default='media/image/default.png',
                               max_length=100, verbose_name='图像', blank=True, null=True)
    image2 = models.ImageField(upload_to='image', default='media/image/default.png',
                               max_length=100, verbose_name='图像', blank=True, null=True)
    image_processed = models.ImageField(upload_to='image/image_processed', default='media/image/default.png',
                                        max_length=100, verbose_name='图像1', blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sift'


class flr_set(models.Model):
    image = models.ImageField(upload_to='image', default='media/image/default.png',
                              max_length=100, verbose_name='图像', blank=True, null=True)
    image_processed = models.ImageField(upload_to='image/image_processed', default='media/image/default.png',
                                        max_length=100, verbose_name='图像1', blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'flr_set'


class al_route(models.Model):
    image = models.ImageField(upload_to='image', default='media/image/white_board.png',
                              max_length=256, verbose_name='图像', blank=True, null=True)
    image_add_points = models.ImageField(upload_to='image/image_processed', default='media/image/default.png',
                                         max_length=256, verbose_name='图像1', blank=True, null=True)
    image_alo = models.ImageField(upload_to='image/image_processed', default='media/image/default.png',
                                  max_length=256, verbose_name='图像1', blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'al_route'


class Pay(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    item_spend = models.CharField(null=False, max_length=50)
    money = models.FloatField(null=False)
    year = models.IntegerField(null=False)
    month = models.IntegerField(null=False)
    day = models.IntegerField(null=False)
    isPri = models.BooleanField(null=False)
    data_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        temp = "id is : " + str(self.id) + "--item is : " + str(self.item_spend)
        return temp


class User(models.Model):
    Email = models.EmailField(unique=True, default='123@163.com', null=False, max_length=128)
    Name = models.CharField(default='xxx', null=False, max_length=128)
    Password = models.CharField(default='123456789', null=False, max_length=128)

    class Meta:
        db_table = 'user'
