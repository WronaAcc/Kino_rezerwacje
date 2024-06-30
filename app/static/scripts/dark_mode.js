document.addEventListener('DOMContentLoaded', function() {
    const toggleDarkMode = document.querySelector('.toggle-dark-mode');
    const toggleThumb = document.querySelector('.toggle-thumb');
    const icons = document.querySelectorAll('.icon');

    function applyDarkMode(isDarkMode) {
        document.body.classList.toggle('dark-mode', isDarkMode);
        toggleThumb.style.left = isDarkMode ? '42px' : '2px';
        icons.forEach(icon => {
            icon.style.opacity = icon.classList.contains('icon-day') ? (isDarkMode ? '1' : '0') : (isDarkMode ? '0' : '1');
        });
    }

    // Sprawdzenie lokalnego storage na temat trybu ciemnego
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    document.body.classList.add('no-transition');
    applyDarkMode(isDarkMode);
    setTimeout(() => document.body.classList.remove('no-transition'), 100);

    toggleDarkMode.addEventListener('click', function() {
        const isDarkMode = !document.body.classList.contains('dark-mode');
        localStorage.setItem('darkMode', isDarkMode);
        applyDarkMode(isDarkMode);
    });
});