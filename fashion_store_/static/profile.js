const user = JSON.parse(localStorage.getItem('user')) || {
  name: 'John Doe',
  email: 'johndoe@example.com'
};

const container = document.getElementById('profile-container');
container.innerHTML = `
  <h2>${user.name}</h2>
  <p><strong>Email:</strong> ${user.email}</p>
  <p><strong>Member since:</strong> January 2024</p>
`;


