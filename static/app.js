async function encryptMessage() {
    const message = document.getElementById("message").value;
    const response = await fetch('/encrypt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: message })
    });

    const data = await response.json();
    document.getElementById("result").innerText = data.encrypted_text;
}

async function decryptMessage() {
    const message = document.getElementById("message").value;
    const response = await fetch('/decrypt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: message })
    });

    const data = await response.json();
    document.getElementById("result").innerText = data.decrypted_text;
}
