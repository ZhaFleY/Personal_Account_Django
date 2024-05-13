document.getElementById("registration").addEventListener("submit", function(event) {
            var password = document.getElementById("password").value;
            var rePassword = document.getElementById("re_password").value;
            if (password !== rePassword) {
                alert("Passwords do not match");
                event.preventDefault(); // Останавливаем отправку формы
            }});



