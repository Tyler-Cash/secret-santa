$(document).ready(function () {
    console.log($('.family-radio:checked').val());
    $("#signup-form").bind('submit', function (e) {
        $.getJSON($SCRIPT_ROOT + '/AJAXsignup', {
            fName: $('input[name="fName"]').val(),
            lName: $('input[name="lName"]').val(),
            email: $('input[name="email"]').val(),
            pass: $('input[name="pass"]').val(),
            uselessPass: $('input[name="uselessPassword"]').val(),
            family: $('.family-radio:checked').val()
        }, function (data) {
            $("#result").removeClass();
            if(!data.success){
                $("#result").addClass("card-panel #ff8a80 red accent-1");
            }else {
                $("#result").addClass("card-panel #b9f6ca green accent-1");
                window.location.href = data.redirect
            }
            $("#result").html(data.outcome);
        });
        return false;
    });
});