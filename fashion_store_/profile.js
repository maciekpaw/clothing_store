
// profile.js
document.addEventListener("DOMContentLoaded", () => {
  const user = JSON.parse(localStorage.getItem("user"));
  const container = document.getElementById("profile-info");
  if (user && container) {
    container.innerHTML = \`
      <p><strong>Name:</strong> \${user.name}</p>
      <p><strong>Email:</strong> \${user.email}</p>
      <button onclick="logout()">Logout</button>
    \`;
  }
});

function logout() {
  localStorage.removeItem("user");
  window.location.href = "index.html";
}
