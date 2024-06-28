document.addEventListener('DOMContentLoaded', function() {
    const seatMap = document.getElementById('seat-map');
    const selectedSeatsInput = document.getElementById('selected_seats');
    const selectedSeats = new Set();

    seatMap.addEventListener('click', function(event) {
        const target = event.target;
        if (target.classList.contains('seat') && !target.classList.contains('reserved')) {
            const seat = target.getAttribute('data-seat');
            if (selectedSeats.has(seat)) {
                selectedSeats.delete(seat);
                target.classList.remove('selected');
            } else {
                selectedSeats.add(seat);
                target.classList.add('selected');
            }
            selectedSeatsInput.value = Array.from(selectedSeats).join(',');
        }
    });
});
