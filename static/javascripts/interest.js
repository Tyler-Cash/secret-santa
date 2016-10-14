$(document).ready(function () {
    $.getJSON($SCRIPT_ROOT + '/ajax-get-interests', {}, function (data) {
        $("#result").removeClass();
        $("#interest-holder").addClass("card-panel #ff8a80 red accent-1");
        var getInterestsFailed = false;
        if (data.success) {
            if (data.outcome.length != 0) {
                var html = "<span class='card-title'>Your interests</span><ul class='collection'>";

                for (var i = 0; i < data.outcome.length; i++) {
                    html += "<li class='collection-item'>" + data.outcome[i][0] + "<a name='interest-delete' id='" + data.outcome[i][1] + "' class='right'>X</a></li>";
                }
                $("#interest-holder").html(html + "</ul>");
            } else {
                getInterestsFailed = true;
            }
        } else {
            getInterestsFailed = true;
        }

        if(getInterestsFailed){
            $("#interest-holder").html("<span class='card-title'>Your interests</span><p>You appear to have no interests yet.</p>");
        }
    });

});