$(document).ready(function() {
    function readURL(input,selector) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $(selector).attr('src', e.target.result);
            };

            reader.readAsDataURL(input.files[0]);
        }
    }
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
    $('#id_avatar').change(function(){
        var data = new FormData();
        $.each($('#id_avatar')[0].files, function(i, file) {
                data.append('uploaded_file', file);
        });
        readURL(this,'.img-polaroid');
    });

    $('#close').click(function(){
        $('#user_data_form').append("<input type='hidden' name='del' value=True />");
        $('.img-polaroid').attr('src', '/static/img/default.png');
    });
});
