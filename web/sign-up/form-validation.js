// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
  'use strict'

  window.addEventListener('load', function () {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation')

    // Loop over them and prevent submission
    Array.prototype.filter.call(forms, function (form) {
      form.addEventListener('submit', function (event) {
        if (form.checkValidity() === false) {
          alert("Please fill in all required fields.")
          event.preventDefault()
          event.stopPropagation()
        }
        else{
          window.location.href = "../sign-in/sign-in.html";
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })
  }, false)
})()

function validatePassword(confirm_password){
  if ($("#password").val() != confirm_password.value){
    confirm_password.setCustomValidity("Password don't match")
  }
  else{
    confirm_password.setCustomValidity("")
  }
}

function showPassword() {
  var x = document.getElementById("password");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}