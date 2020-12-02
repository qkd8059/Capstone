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
          var obj, dbParam, xmlhttp, appetite = "";
          obj = { cookie: document.cookie };
          dbParam = JSON.stringify(obj);
          xmlhttp = new XMLHttpRequest();
          xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
              appetite = JSON.parse(this.responseText);
              alert("According to the survey, your risk appetite is " + appetite)
              event.preventDefault()
              event.stopPropagation()
            }
          }
          xmlhttp.open("POST", "backend/risk-survey/", true);
          xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
          xmlhttp.send(dbParam);
        }

        form.classList.add('was-validated')
      }, false)
    })
  }, false)
})()
