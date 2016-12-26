// Hide prediction result on page load
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
});
