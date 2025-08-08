const btnOpenLogin = document.getElementById("openModal");
const modalLogin = document.getElementById("modalLogin");
const closeLogin = document.getElementById("closeLogin");

const modalRegister = document.getElementById("modalRegister");
const closeRegister = document.getElementById("closeRegister");
const goRegister = document.getElementById("goRegister");
const goLogin = document.getElementById("goLogin");


// Abrir Login
btnOpenLogin.addEventListener("click", () => {
  modalLogin.style.display = "flex";
});

// Cerrar Login
closeLogin.addEventListener("click", () => {
  modalLogin.style.display = "none";
});

// Ir a registro desde login
goRegister.addEventListener("click", () => {
  modalLogin.style.display = "none";
  modalRegister.style.display = "flex";
});

// Ir a login desde registro
goLogin.addEventListener("click", () => {
    modalRegister.style.display = "none";
    modalLogin.style.display = "flex";
    });

// Cerrar Registro
closeRegister.addEventListener("click", () => {
  modalRegister.style.display = "none";
});

// Cerrar si hacen clic fuera del modal
[modalLogin, modalRegister].forEach(modal => {
  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });
});
