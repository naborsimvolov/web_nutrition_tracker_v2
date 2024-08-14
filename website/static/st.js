function displayMessage(message, category) {
    const messageContainer = document.getElementById('messageContainer');
    messageContainer.innerHTML = `<div class='alert alert-${category}'>${message}</div>`;

    // Automatically hide the message after 5 seconds
    setTimeout(() => {
        messageContainer.innerHTML = '';
    }, 5000);
}
