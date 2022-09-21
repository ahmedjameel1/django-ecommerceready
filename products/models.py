from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=250, blank=True, null=True)
    price = models.IntegerField()
    stock = models.IntegerField()
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=50, unique=True)
    image = models.ImageField(default="", upload_to="products/%y/%m/%d")
    created = models.DateTimeField(auto_now_add=True,editable=False)
    modified = models.DateTimeField(auto_now=True)
    #category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __STR__(self):
        return self.title

    