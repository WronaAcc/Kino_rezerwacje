document.querySelectorAll('.seat').forEach(seat => {
    seat.addEventListener('click', function() {
        if (!this.classList.contains('reserved')) {
            this.classList.toggle('selected');
            updateSelectedSeats();
        }
    });
});

function updateSelectedSeats() {
    const selectedSeats = Array.from(document.querySelectorAll('.seat.selected')).map(seat => seat.dataset.seat);
    document.getElementById('selected_seats').value = selectedSeats.join(',');
}
