$(document).ready(function () {
    $("#login-form").bind('submit', function (e) {
        $.getJSON($SCRIPT_ROOT + '/ajaxlogin', {
            email: $('input[name="email"]').val(),
            first_name: $('input[name="first-name"]').val()

        }, function (data) {
            $("#result").removeClass();
            if (!data.success) {
                $("#result").addClass("card-panel #ff8a80 red accent-1");

            } else {
                $("#result").addClass("card-panel #b9f6ca green accent-1");
                Cookies.set('user_secret', data.user_secret);
                window.location.href = data.redirect;
            }
            $("#result").html(data.outcome);
        });
        return false;
    });
});
