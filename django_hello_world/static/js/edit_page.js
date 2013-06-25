$(document).ready(function() {
    $()
    var options = {
        beforeSubmit:function () {
                $("#loader").css("display", "block");
                return true;
        },
        success:function(responseText)  {
                $("#loader").css("display", "none");
                $('#user_data_form').find('input, textarea, button').removeAttr('disabled');
                var modal =  $('.alert');
                if (responseText.success) {
                    modal.attr('class', 'alert alert-success fade in');
                } else {
                    modal.attr('class', 'alert alert-error fade in');
                }
                modal.text(responseText.message);
                modal.fadeIn(300).delay(3000).slideUp(300);

        }
    };

    $('#user_data_form').submit(function() {
        $(this).ajaxSubmit(options);
        $('#user_data_form').find('input, textarea, button').attr('disabled','disabled');
        return false;
     });
});
