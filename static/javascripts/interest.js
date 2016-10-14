$(document).ready(function () {
    $.getJSON($SCRIPT_ROOT + '/ajax-get-interests', {}, function (data) {
        $("#result").removeClass();
        $("#interest-holder").addClass("card-panel #ff8a80 red accent-1");
        var getInterestsFailed = false;
        if (data.success) {
            if (data.outcome.length != 0) {
                var html = "<span class='card-title'>Your interests</span><ul class='collection'>";

                for (var i = 0; i < data.outcome.length; i++) {
                    html += "<li class='collection-item black-text'>" + data.outcome[i][0] + "<span id='" + data.outcome[i][1] + "' class='right red-text interest-delete'>X</span></li>";
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

    $(document).on('click', '.interest-delete', function (element) {
        console.log(element);
        var interest_id = element.target.id;

        $.getJSON($SCRIPT_ROOT + '/ajax-delete-interest-' + interest_id, {}, function (data) {
            if (data.success) {
                $("#" + interest_id).parent().remove();
            }else {
                Materialize.toast("Can\'t remove interest, please email contact@tylercash.xyz");
            }
        });
    });
});