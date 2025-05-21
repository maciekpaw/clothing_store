const params = new URLSearchParams(window.location.search);
const name = params.get('name');
const price = parseFloat(params.get('price'));
const image = params.get('image');

const container = document.getElementById('product-container');

if (name && price && image) {
  container.innerHTML = `
    <section class="product-detail">
      <img src="${image}" alt="${name}" />
      <div class="product-detail-info">
        <h2>${name}</h2>
        <p><strong>Price:</strong> $${price.toFixed(2)}</p>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Urban fit. Street edge.</p>
        <button onclick="addToCart('${name}', ${price}, '${image}')">Add to Cart</button>
      </div>
    </section>
  `;
} else {
  container.innerHTML = '<p>Product not found.</p>';
}

function addToCart(name, price, image) {
  const cart = JSON.parse(localStorage.getItem('cart')) || [];
  cart.push({ name, price, image });
  localStorage.setItem('cart', JSON.stringify(cart));
  alert(name + ' added to cart.');
}


