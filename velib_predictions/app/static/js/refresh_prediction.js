$(function(){
    $("#prediction-result").hide()
})

$('#prediction-form').submit(function(e){
    e.preventDefault();
    $.post(
        'prediction',
        {
            number_station: $('#number_station').val()
        },
        function(data){
            prediction = data['prediction']
            $("#prediction").text(prediction)
            $("#prediction-result").show()

//            // Hide evaluation box if errors box is not empty
//            if ( $('#errors-box').css("display") == 'block' ) {
//                $('#prediction-result').hide();
//            } else {
//                $("#prediction-result").show()
//            }
        }
    );
});
