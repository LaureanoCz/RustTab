    document.addEventListener("DOMContentLoaded", () => {
        const closeBtn = document.querySelector(".close-btn");
        const errorBox = document.querySelector(".error-message");

        if (closeBtn) {
            closeBtn.addEventListener("click", () => {
                errorBox.style.display = "none";
                closeBtn.style.display = "none";
            });
        }
    });