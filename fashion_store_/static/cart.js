function addToCart(product) {
  if (!product.name || !product.price || !product.img) {
    alert("Produkt nie zawiera wszystkich wymaganych danych.");
    return;
  }
  
  const loggedUser = localStorage.getItem("loggedUser");
  if (!loggedUser) {
    showLoginRequiredModal();
    return;
  }

  const cartKey = `cart_${loggedUser}`;
  const cart = JSON.parse(localStorage.getItem(cartKey)) || [];
  cart.push(product);
  localStorage.setItem(cartKey, JSON.stringify(cart));
  showAddConfirmation(product.name);
}

function loadCart() {
  const loggedUser = localStorage.getItem("loggedUser");
  const cartKey = loggedUser ? `cart_${loggedUser}` : "cart";
  const cartItems = JSON.parse(localStorage.getItem(cartKey)) || [];
  const container = document.getElementById("cart-container");
  if (!container) return;
  container.innerHTML = "";

  if (cartItems.length === 0) {
    container.innerHTML = "<p>Your cart is empty.</p>";
    return;
  }

  cartItems.forEach((item, index) => {
    const div = document.createElement("div");
    div.className = "cart-item";
    div.innerHTML = `
      <img src="${item.img}" alt="${item.name}" style="height: 100px;">
      <p>${item.name}</p>
      <p>$${item.price}</p>
      <button onclick="removeItem(${index})">Remove</button>
    `;
    container.appendChild(div);
  });
}

function removeItem(index) {
  const loggedUser = localStorage.getItem("loggedUser");
  const cartKey = loggedUser ? `cart_${loggedUser}` : "cart";
  let cart = JSON.parse(localStorage.getItem(cartKey)) || [];
  cart.splice(index, 1);
  localStorage.setItem(cartKey, JSON.stringify(cart));
  loadCart();
}

document.addEventListener("DOMContentLoaded", loadCart);


