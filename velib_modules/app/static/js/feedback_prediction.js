$('#feedback-form').submit(function(){
    $.post(
    'feedback',
        {
        feedback: $('#feedback').val()
        // available_bikes : $('#feedback').val()  // $("#available_bikes").val(),
        }
    );
})

