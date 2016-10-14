$(document).ready(function () {
    $.getJSON($SCRIPT_ROOT + '/ajax-get-interests', {
    }, function (data) {
        $("#result").removeClass();
        if (!data.success) {
            $("#interest-holder").addClass("card-panel #ff8a80 red accent-1");
            $("#interest-holder").html("<p>Error, couldn't get interests from server</p>");
        } else {
            $("#result").addClass("card-panel #b9f6ca green accent-1");
            $("#interest-holder").html(data.outcome);
        }
    });

});