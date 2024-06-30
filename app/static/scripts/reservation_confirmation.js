document.addEventListener('DOMContentLoaded', function() {
    const reservationForm = document.getElementById('reservation-form');

    reservationForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(reservationForm);

        fetch(reservationForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show animation and thank you message
                    const thankYouMessage = document.createElement('div');
                    thankYouMessage.classList.add('thank-you-animation');
                    thankYouMessage.innerHTML = `
                    <h2>Thank you for your reservation!</h2>
                    <p>${data.message}</p>
                    <p>A confirmation email has been sent to your email address with the ticket number. Please show it at the entrance.</p>
                `;
                    document.body.appendChild(thankYouMessage);

                    setTimeout(() => {
                        window.location.href = "/profile";
                    }, 5000);
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('There was an error with your reservation. Please try again.');
            });
    });
});