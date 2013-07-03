show_list = function(data){
    $('#list_container').append(data);
    $('#list_param_form').find('input, textarea, button').removeAttr('disabled');
    $('.priority').change(function(event) {
        $.ajax({
            url: '/requests/change_priority/',
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                id: event.target.id,
                value: event.target.value
            },
            type: 'POST',
            success: function(responseText)  {
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
        });
    });
    $('.sort').click(function(event) {
        $("#list_container").empty();
        start = $('#start').find(":selected").text();
        end = $('#end').find(":selected").text();
        $.ajax({
            url: '/requests/sort/',
            data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                id: event.target.id,
                type: event.target.className.split(" ")[1],
                start: start,
                end: end
            },
            type: 'POST',
            success: show_list
        });
    });

};

$(document).ready(function() {
    $.ajax({
        url: '/requests/list/',
        data: {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
        type: 'POST',
        success: show_list
    });

    var options = {
        beforeSubmit:function () {
                $("#list_container").empty();
                return true;
        },
        success: show_list
    };

    $('#list_param_form').submit(function() {
        $(this).ajaxSubmit(options);
        $('#list_param_form').find('input, textarea, button').attr('disabled','disabled');
        return false;
     });
});
