document.getElementById('toggleButton').addEventListener('click', function() {
    var panel = document.getElementById('panel');
    if (panel.style.display === 'none') {
        panel.style.display = 'block';
    } else {
        panel.style.display = 'none';
    }
});
