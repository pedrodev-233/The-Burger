from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .models import Order, Product


def home(request):
    products = Product.objects.filter(active=True).order_by('category', 'name')
    recent_orders = Order.objects.select_related('product').order_by('-created_at')[:8]
    context = {
        'products': products,
        'recent_orders': recent_orders,
        'order_count': Order.objects.count(),
        'ready_orders': Order.objects.filter(status='pronto').count(),
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'core/index.html', context)


def pedido(request):
    if request.method != 'POST':
        return redirect('home')

    product_id = request.POST.get('product')
    customer_name = request.POST.get('customer_name', '').strip()
    phone = request.POST.get('phone', '').strip()
    address = request.POST.get('address', '').strip()
    notes = request.POST.get('notes', '').strip()
    quantity = int(request.POST.get('quantity', 1) or 1)

    if not all([product_id, customer_name, phone, address]):
        messages.error(request, 'Preencha nome, telefone e endereço para concluir o pedido.')
        return redirect('home')

    product = get_object_or_404(Product, pk=product_id, active=True)
    order = Order.objects.create(
        product=product,
        customer_name=customer_name,
        phone=phone,
        address=address,
        quantity=quantity,
        notes=notes,
    )
    messages.success(
        request,
        f'Pedido #{order.id} de {product.name} registrado com sucesso!'
    )
    return redirect('home')


@user_passes_test(lambda user: user.is_superuser, login_url='/admin/login/')
@login_required(login_url='/admin/login/')
def hamburgueria(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')
        if order_id and status:
            order = get_object_or_404(Order, pk=order_id)
            if status in dict(Order.STATUS_CHOICES):
                order.status = status
                order.save(update_fields=['status', 'updated_at'])
                messages.success(request, f'Status do pedido #{order.id} atualizado para {order.get_status_display()}.')
        return redirect('hamburgueria')

    orders = Order.objects.select_related('product').order_by('-created_at')
    summary = {
        'total': orders.count(),
        'pendentes': orders.filter(status='pendente').count(),
        'em_preparo': orders.filter(status='em_preparo').count(),
        'prontos': orders.filter(status='pronto').count(),
        'entregues': orders.filter(status='entregue').count(),
    }
    context = {
        'orders': orders,
        'summary': summary,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'core/hamburgueria.html', context)