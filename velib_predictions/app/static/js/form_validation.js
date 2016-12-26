$(document).ready(function(){
  $("#prediction-form").validate({
    rules: {
        number_station: {
            required: true,
            digits: true
        }
    },
    messages: {
        number_station: {
            required: "Veuillez renseigner un numéro de station",
            digits: "Le numéro de station doit être un nombre entier"
        }
    },
    errorLabelContainer: '#errors-box',
    errorElement: 'div',
  });
});

