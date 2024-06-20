const container = document.getElementById("container");
const registerBtn = document.getElementById("register");
const loginBtn = document.getElementById("login");

registerBtn.addEventListener("click", () => {
  container.classList.add("active");
});

loginBtn.addEventListener("click", () => {
  container.classList.remove("active");
});

// section selection

document.addEventListener("DOMContentLoaded", function () {
  // Check if we should scroll to the services section
  if (window.ScrollLogin) {
    document.getElementById("signup").scrollIntoView({ behavior: "smooth" });
    container.classList.remove("active");
  }
  if (window.ScrollSignin) {
    document.getElementById("signup").scrollIntoView({ behavior: "smooth" });
    container.classList.add("active");
  }
});
