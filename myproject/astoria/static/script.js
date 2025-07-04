document.getElementById('leadForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const form = new FormData(this);
    const data = Object.fromEntries(form.entries());

    const response = await fetch('/submit/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    document.getElementById('status').innerText = result.message;
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}