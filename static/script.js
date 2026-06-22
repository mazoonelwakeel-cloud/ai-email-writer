async function generateEmail() {

    const purpose = document.getElementById("purpose").value;
    const recipient = document.getElementById("recipient").value;
    const sender = document.getElementById("sender").value;
    const language = document.getElementById("language").value;
    const tone = document.getElementById("tone").value;
    const length = document.getElementById("length").value;

    const output = document.getElementById("output");

    output.value = "Generating email...";

    try {

        const response = await fetch("/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                purpose,
                recipient,
                sender,
                language,
                tone,
                length
            })
        });

        const data = await response.json();

        if (data.success) {
            output.value = data.email;
        } else {
            output.value = "Error: " + data.error;
        }

    } catch (error) {
        output.value = "Connection error.";
    }
}