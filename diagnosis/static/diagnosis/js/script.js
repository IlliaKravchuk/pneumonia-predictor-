function submitForm() {
    const input = document.getElementById('id_image');
    const btn = document.querySelector('.btn');

    if (input.files.length > 0) {
        btn.style.opacity = '0.5';
        btn.innerText = 'Аналізуємо...';

        document.getElementById('upload-form').submit();
    }
}