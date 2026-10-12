const formatMoney = (value) =>
  new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(value);

const productSelect = document.getElementById('product');
const quantityInput = document.getElementById('quantity');
const productNameEl = document.getElementById('selected-product-name');
const productPriceEl = document.getElementById('selected-product-price');
const orderQtyEl = document.getElementById('order-qty');
const orderTotalEl = document.getElementById('order-total');

const updateOrderSummary = () => {
  if (!productSelect || !quantityInput || !productNameEl || !productPriceEl || !orderQtyEl || !orderTotalEl) {
    return;
  }

  const selectedOption = productSelect.options[productSelect.selectedIndex];
  if (!selectedOption) {
    return;
  }

  const quantity = Math.max(1, Number(quantityInput.value || 1));
  const price = Number(selectedOption.dataset.price || 0);
  const total = price * quantity;

  productNameEl.textContent = selectedOption.dataset.name || '';
  productPriceEl.textContent = formatMoney(price);
  orderQtyEl.textContent = quantity;
  orderTotalEl.textContent = formatMoney(total);
};

if (productSelect && quantityInput) {
  productSelect.addEventListener('change', updateOrderSummary);
  quantityInput.addEventListener('input', updateOrderSummary);
  updateOrderSummary();
}

const menuToggle = document.querySelector('.menu-toggle');
const siteNav = document.getElementById('site-nav');

if (menuToggle && siteNav) {
  menuToggle.addEventListener('click', () => {
    const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
    menuToggle.setAttribute('aria-expanded', String(!isExpanded));
    siteNav.classList.toggle('menu-open');
  });
}