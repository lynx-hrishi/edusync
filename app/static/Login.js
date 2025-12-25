const loginBtn = document.getElementById("login-btn");
const errorMsg = document.getElementById("error-msg");
loginBtn.addEventListener("click",async (e) => {
    e.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const errorMsg = document.getElementById("errorMsg");

    errorMsg.textContent = "";

    let BACKENDURL = "https://fluffy-heidi-monoprotic.ngrok-free.dev";

    try {
        const loginData = new FormData();

        const payload = { email, password };
        loginData.append("payload", JSON.stringify(payload));

        const response = await fetch(`${BACKENDURL}/api/auth/login`, {
            method: "POST",
            body: loginData
        });

        const data = await response.json();

        if (!response.ok) {
            errorMsg.textContent = data.error || "Login failed";
            return;
        }

    } catch (err) {
        errorMsg.textContent = "Server error";
    }
})