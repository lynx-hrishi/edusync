const registerbtn = document.getElementById("register-btn");
const error = document.getElementById("error-msg-reg");

registerbtn.addEventListener("click", async (e) => {
    e.preventDefault()

    const name = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const age = document.getElementById('age').value;
    const password = document.getElementById('password').value;
    // const error = document.getElementById('error')/;

    error.textContent = "";

    let BACKENDURL = "https://fluffy-heidi-monoprotic.ngrok-free.dev";

    try {
        const registerData = new FormData();

        const payload = { name, age, email, password };
        registerData.append("payload", JSON.stringify(payload));

        const response = await fetch(`/api/auth/register`, {
            method: "POST",
            body: registerData
        });

        const data = await response.json();

        if (!response.ok) {
            error.textContent = data.message || "Register failed";
            return;
        }

        // Redirect to goals page after successful registration
        window.location.href = "/pref";

    } catch (err) {
        error.textContent = "Server error"
    }
})