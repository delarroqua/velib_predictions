$(function() {
  $("form[name='prediction-form']").validate({
    rules: {
        number_station: {
            required: true,
            digits: true
        }
    },
    number_station: {
        number_station: {
            required: "Veuillez renseigner un numéro de station",
            digits: "Le numéro de station doit être un nombre entier"
        }
    },
    // errorLabelContainer: '#errors-box',
    // errorElement: 'div',
  });
});

