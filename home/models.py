from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('burger', 'Burger'),
        ('acompanhamento', 'Acompanhamento'),
        ('bebida', 'Bebida'),
    ]

    name = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='burger')
    image_url = models.URLField(blank=True, default='')
    is_featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_preparo', 'Em preparo'),
        ('pronto', 'Pronto'),
        ('entregue', 'Entregue'),
    ]

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orders')
    customer_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=25)
    address = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.customer_name} - {self.product.name}'