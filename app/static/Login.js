async function handleLogin() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const errorMsg = document.getElementById("errorMsg");

    errorMsg.textContent = "";

    let BACKENDURL = "https://fluffy-heidi-monoprotic.ngrok-free.dev";

    try {
        const response = await fetch(`${BACKENDURL}/api/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            errorMsg.textContent = data.error || "Login failed";
            return;
        }

    } catch (err) {
        errorMsg.textContent = "Server error";
    }
}