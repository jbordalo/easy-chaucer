const themeToggle = document.getElementById('themeToggle');
    const body = document.body;
    const fontSizeSlider = document.getElementById('fontSize');
    const fontSelect = document.getElementById('fontSelect');

    fontSizeSlider.addEventListener('input', updateStyle);
    fontSelect.addEventListener('change', updateStyle);

    if (localStorage.getItem('theme') !== null) {
        console.log("Setting theme:", localStorage.getItem('theme'));
        body.classList.add(localStorage.getItem('theme'));
    } else {
        body.classList.add('dark');
        localStorage.setItem('theme', 'dark')
    }

    document.addEventListener("DOMContentLoaded", function() {
        const container = document.querySelector('.container');
        
        if (localStorage.getItem('fontSize')) {
            const fontSize = localStorage.getItem('fontSize');

            container.style.fontSize = fontSize + 'px';
            fontSizeSlider.value = fontSize;
        }
        if (localStorage.getItem('fontFamily')) {
            const fontFamily = localStorage.getItem('fontFamily');

            container.style.fontFamily = fontFamily;
            fontSelect.value = fontFamily;
        }

        container.style.visibility = "visible";
    })

    themeToggle.addEventListener('click', () => {
        console.log("Switching theme");

        if (body.classList.contains('light')) {
            body.classList.replace('light', 'dark');
            localStorage.setItem('theme', 'dark');
        } else if (body.classList.contains('dark')) {
            body.classList.replace('dark', 'sepia');
            localStorage.setItem('theme', 'sepia');
        } else {
            body.classList.replace('sepia', 'light');
            localStorage.setItem('theme', 'light');
        }
    });

    function updateStyle() {
        const container = document.querySelector('.container');

        const fontSize = fontSizeSlider.value;
        const fontFamily = fontSelect.value;

        container.style.fontSize = fontSize + 'px';
        container.style.fontFamily = fontFamily;

        localStorage.setItem('fontSize', fontSize);
        localStorage.setItem('fontFamily', fontFamily);
    }