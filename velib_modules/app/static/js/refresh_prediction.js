$(document).ready(function() {
    $('#errors-box').empty().hide();
    $("#prediction-result").hide()

    $('#prediction-form').submit(function(e){
        e.preventDefault();
        $.post(
            'prediction',
            {
                number_station: $('#number_station').val(),
                time_prediction: $('#time_prediction').val()
            },
            function(data){
                available_bikes = data['available_bikes']
                available_spots = data['bike_stands'] - available_bikes
                $("#available_bikes").text(available_bikes)
                $("#available_spots").text(available_spots)
            }
        );
        // Hide evaluation box if there is errors box is not empty
        $(function(){
            if ($('#errors-box').html().length == 0) {
                $("#prediction-result").show()
                $('#errors-box').hide()
            } else {
                $('#prediction-result').hide();
                $('#errors-box').show()
            }
        })
    })
});
