async function handleRegister() {
    const name = document.getElementById('username');
    const email = document.getElementById('email');
    const number = document.getElementById('mobile');
    const password = document.getElementById('password');
    const error = document.getElementById('error');

    error.textContent = "";

    let BACKENDURL = "https://fluffy-heidi-monoprotic.ngrok-free.dev";

    try {
        const response = await fetch(`${BACKENDURL}/api/auth/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name, email, number, password })
        });

        const data = await response.json();

        if (!response.ok) {
            error.textContent = data.error || "Register failed";
            return;
        }

    } catch (err) {
        error.textContent = "Server error"
    }
}