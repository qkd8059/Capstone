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
          alert("Please answer all questions in the survey.")
          event.preventDefault()
          event.stopPropagation()
        }
        else {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
        location.href = "../dashboard/dashboard.html"
      }, false)
    })
  }, false)
})()
