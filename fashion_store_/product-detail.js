
// product-detail.js
document.addEventListener("DOMContentLoaded", () => {
  const product = {
    name: "Black Hoodie",
    price: "$79.99",
    img: "https://images.unsplash.com/photo-1618354691390-01ccf7a6b6ba?auto=format&fit=crop&w=400&q=80"
  };
  const container = document.getElementById("product-detail");
  const suggestions = [
    {
      name: "White T-Shirt",
      price: "$49.99",
      img: "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=400&q=80"
    },
    {
      name: "Green Jacket",
      price: "$119.99",
      img: "https://images.unsplash.com/photo-1520975916090-3105956dac38?auto=format&fit=crop&w=400&q=80"
    }
  ];

  container.innerHTML = \`
    <div style="display:flex;gap:2rem;flex-wrap:wrap;">
      <img src="\${product.img}" style="max-width:100%;border-radius:8px;">
      <div style="flex:1;">
        <h2>\${product.name}</h2>
        <p><strong>\${product.price}</strong></p>
        <p>Minimalistic premium cotton hoodie. Perfect for everyday wear.</p>
        <button onclick='addToCart(\${JSON.stringify(product)})'>Add to Cart</button>
      </div>
    </div>
    <h3>Similar Products</h3>
    <div class="grid">
      \${suggestions.map(p => \`
        <div class="product-card">
          <img src="\${p.img}">
          <p>\${p.name}</p>
          <p>\${p.price}</p>
        </div>
      \`).join("")}
    </div>
  \`;
});
