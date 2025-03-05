document.addEventListener('DOMContentLoaded', function() {
    const themeToggleButton = document.querySelector('#theme-toggle-button');
    const body = document.body;

    // Get the value of a cookie by name
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    // Set a cookie
    function setCookie(name, value, days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        document.cookie = `${name}=${value}; expires=${date.toUTCString()}; path=/`;
    }

    // Apply initial theme from cookie or default to 'light'
    const currentTheme = getCookie('theme') || 'light';
    body.classList.add(currentTheme);
    themeToggleButton.innerHTML = currentTheme === 'light' ? '🌙' : '☀️';

    // Toggle theme on button click
    themeToggleButton.addEventListener('click', function() {
        if (body.classList.contains('light')) {
            body.classList.replace('light', 'dark');
            themeToggleButton.innerHTML = '☀️';
            setCookie('theme', 'dark', 30); // Save for 30 days
        } else {
            body.classList.replace('dark', 'light');
            themeToggleButton.innerHTML = '🌙';
            setCookie('theme', 'light', 30);
        }
    });
});
