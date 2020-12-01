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
          window.location.href = "../dashboard/dashboard.html";
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })
  }, false)
})()

function validateEndDate(end_date){
  start_date = $("#start-date").val()
  if (end_date.value > start_date){
    end_date.setCustomValidity("")
  }
  else{
    end_date.setCustomValidity("Invalid end date")
  }
}
