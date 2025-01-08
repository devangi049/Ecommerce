from django.db import models
from .category import Category

class Product(models.Model):
    name=models.CharField(max_length=50)
    price=models.IntegerField(default=0)
    discount=models.IntegerField(default=0)
    # category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    description=models.CharField(max_length=200,null=True,blank=True,default="")
    image1=models.ImageField(upload_to="uploads/products", blank=False, null=True)
    image2=models.ImageField(upload_to="uploads/products",  blank=True, null=True)
    image3=models.ImageField(upload_to="uploads/products",  blank=True, null=True)
    image4=models.ImageField(upload_to="uploads/products",  blank=True, null=True)
    image5=models.ImageField(upload_to="uploads/products",  blank=True, null=True)
    
    
    @staticmethod
    
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    
    def get_all_products():
        return Product.objects.all()
    
    @staticmethod
    
    def get_all_products_by_categories_id(category_id):
        if category_id:
         
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()


    def __str__(self):
        return self.name