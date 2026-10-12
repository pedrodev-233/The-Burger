from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Order, Product

User = get_user_model()


class BurgerFlowTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='O da Casa',
            description='Clássico com queijo e molho da casa.',
            price=32.00,
            category='burger',
            is_featured=True,
        )
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@theburger.com',
            password='senha123',
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'O da Casa')

    def test_can_create_order(self):
        response = self.client.post(
            reverse('pedido'),
            {
                'product': self.product.id,
                'customer_name': 'Carlos',
                'phone': '11999999999',
                'address': 'Rua da Brasa, 10',
                'quantity': 2,
                'notes': 'Sem cebola',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.first().quantity, 2)

    def test_hamburgueria_requires_superuser_login(self):
        response = self.client.get(reverse('hamburgueria'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

        self.client.force_login(self.superuser)
        response = self.client.get(reverse('hamburgueria'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Área da Hamburgueria')

    def test_can_update_order_status(self):
        order = Order.objects.create(
            product=self.product,
            customer_name='Maria',
            phone='11988888888',
            address='Av. Paulista, 200',
            quantity=1,
        )

        self.client.force_login(self.superuser)
        response = self.client.post(
            reverse('hamburgueria'),
            {'order_id': order.id, 'status': 'pronto'},
        )

        self.assertEqual(response.status_code, 302)
        order.refresh_from_db()
        self.assertEqual(order.status, 'pronto')
