
// auth.js
document.addEventListener("DOMContentLoaded", function () {
  const signupForm = document.getElementById("signup-form");
  const loginForm = document.getElementById("login-form");

  if (signupForm) {
    signupForm.onsubmit = (e) => {
      e.preventDefault();
      const email = signupForm.email.value;
      const password = signupForm.password.value;
      const name = signupForm.name.value;
      localStorage.setItem("user", JSON.stringify({ email, name }));
      window.location.href = "profile.html";
    };
  }

  if (loginForm) {
    loginForm.onsubmit = (e) => {
      e.preventDefault();
      const email = loginForm.email.value;
      const password = loginForm.password.value;
      const user = JSON.parse(localStorage.getItem("user"));
      if (user && user.email === email) {
        window.location.href = "profile.html";
      } else {
        alert("Invalid credentials.");
      }
    };
  }
});
