$(document).ready(function() {
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

        data.append('csrfmiddlewaretoken',document.getElementsByName('csrfmiddlewaretoken')[0].value);

        $.ajax({
            url: '/profile/upload_file/',
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            type: 'POST',
            success: function(data){
                $('.img-polaroid').attr('src',data);
            }
        });
    });

    $('#close').click(function(){
        $.ajax({
            type: 'POST',
            url: '/profile/delete_file/',
            data:{ csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
            success: function(data){
                $('#id_uploaded_file').val('');
                $('.img-polaroid').attr('src',data);
            }
        });
    });
});
