$(document).ready(function () {
    $.getJSON($SCRIPT_ROOT + '/ajax-get-interests', {
    }, function (data) {
        $("#result").removeClass();
        $("#interest-holder").addClass("card-panel #ff8a80 red accent-1");
        if (!data.success) {

            $("#interest-holder").html("<p>Error, couldn't get interests from server</p>");
        } else {
            var html = "<span class='card-title'>Your interests</span><ul class='collection'>";

            for(var i =0; i < data.outcome.length; i++){
                html += "<li class='collection-item'>" + data.outcome[i][0] + "<a name='interest-delete' id='" + data.outcome[i][1] +"' class='right'>X</a></li>";
            }
            $("#interest-holder").html(html + "</ul>");
        }
    });

});