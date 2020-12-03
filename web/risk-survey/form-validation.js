// Example starter JavaScript for disabling form submissions if there are invalid fields

function determineRisk() {
  PositiveQ = ["question1", "question2", "question3", "question5", "question12", "question14", "question15", "question16", "question17", "question18", "question19", "question20"]
  NegativeQ = ["question4", "question6", "question7", "question8", "question9", "question10", "question11", "question13"]

  function survey_points(index) {
    if (index <= 4 && index >= 0) {
      return index - 2
    }
    else {
      return 0;
    }
  }

  counter = 0
  for (i = 0; i < PositiveQ.length; i++) {
    for (j = 0; j < 5; j++) {
      if (document.getElementsByName(PositiveQ[i])[j].checked == true) {
        counter += survey_points(j);
      }
    }
  }
  for (i = 0; i < NegativeQ.length; i++) {
    for (j = 0; j < 5; j++) {
      if (document.getElementsByName(NegativeQ[i])[j].checked == true) {
        counter -= survey_points(j);
      }
    }
  }
  if (counter > 10) {
    return "Your preference is: Risk Seeking"
  }
  else if (counter < -10) {
    return "Your preference is: Risk Averse"
  }
  else {
    return "Your preference is: Neither risk averse nor risk seeking"
  }



}

(function () {
  'use strict'

  window.addEventListener('load', function () {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation')

    // Loop over them and prevent submission
    Array.prototype.filter.call(forms, function (form) {
      form.addEventListener('submit', function (event) {
        event.preventDefault()
        event.stopPropagation()
        if (form.checkValidity()) {
          var risk = determineRisk();
          document.getElementById("answer_chunk").innerHTML = risk;
        }

        form.classList.add('was-validated')
      }, false)
    })
  }, false)
})()
