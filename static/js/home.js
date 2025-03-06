 // Optional JavaScript for additional interactivity
 document.addEventListener('DOMContentLoaded', () => {
    // Example: Adding hover effects or dynamic interactions
    const navLinks = document.querySelectorAll('.nav-links a');
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', (e) => {
            e.target.style.backgroundColor = 'rgba(255,255,255,0.2)';
        });
        link.addEventListener('mouseleave', (e) => {
            e.target.style.backgroundColor = 'transparent';
        });
    });
});