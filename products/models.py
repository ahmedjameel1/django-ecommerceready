from django.db import models


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=250, blank=True, null=True)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=50, unique=True)
    image = models.ImageField(default="default-store-350x350.jpg", upload_to="products/%y/%m/%d")
    created = models.DateTimeField(auto_now_add=True,editable=False)
    modified = models.DateTimeField(auto_now=True)
    #category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = "/images/default-store-350x350.jpg"
        return url
    
    
VARIATIONS_CHOICES = (
    ('color','color'),
    ('capacity','capacity'),
)

class VariationsManger(models.Manager):

    def colors(self):
        return super(VariationsManger, self).filter(variation_category='color',is_active=True)
    
    def sizes(self):
        return super(VariationsManger, self).filter(variation_category='capacity',is_active=True)


class Variations(models.Model):
    product            = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100,choices=VARIATIONS_CHOICES)
    is_active          = models.BooleanField(default=True)
    created_date       = models.DateTimeField(auto_now=True)
    
    
    objects = VariationsManger()
    
    def __str__(self):
        return str(self.variation_value)
    