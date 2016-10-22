function build_interests() {
    $.getJSON($SCRIPT_ROOT + '/ajax-get-interests', {}, function (data) {
        var getInterestsFailed = false;
        if (data.success) {
            if (data.outcome.length != 0) {
                var html = "<ul class='collection'>";

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

        if (getInterestsFailed) {
            $("#interest-holder").html("<p>You appear to have no interests yet.</p>");
        }
    });

    $.getJSON($SCRIPT_ROOT + '/ajax-get-recipients-interests', {}, function (data) {
        var getInterestsFailed = false;
        if (data.success) {
            if (data.outcome.length != 0) {
                var html = "<ul class='collection'>";

                for (var i = 0; i < data.outcome.length; i++) {
                    html += "<li class='collection-item black-text'>" + data.outcome[i][0] + "</li>";
                }
                $("#recipients-interests").html(html + "</ul>");
            } else {
                getInterestsFailed = true;
            }
        } else {
            getInterestsFailed = true;
        }

        if (getInterestsFailed) {
            $("#recipients-interests").html("<p>Your recipient appears to have not provided any interests.</p>");
        }
    });
}
$(document).ready(function () {
    //    'main
    build_interests();

    $(document).on('click', '.interest-delete', function (element) {
        console.log(element);
        var interest_id = element.target.id;

        $.getJSON($SCRIPT_ROOT + '/ajax-delete-interest-' + interest_id, {}, function (data) {
            if (data.success) {
                $("#" + interest_id).parent().remove();
            } else {
                Materialize.toast("Can\'t remove interest, please email contact@tylercash.xyz", 5000);
            }
        });

        build_interests();
    });


    $("#add-interest").bind('submit', function (e) {
        $("#add-interest-form").addClass("loading");
        $("#add-interest-form").prop("disabled", true);
        $("#add-interest-form").attr("placeholder", "Sending interest...");
        $.getJSON($SCRIPT_ROOT + '/ajax-add-interest', {
            description: $('input[name="new-interest"]').val(),
        }, function (data) {
            if (!data.success) {
                Materialize.toast(data.reason, 4000);
            } else {

            }
            $("#result").html(data.outcome);
            $("#add-interest-form").removeClass("loading");
            $("#add-interest-form").prop("disabled", false);
            $("#add-interest-form").attr("placeholder", "Insert an interest (e.g. programming)");
        });
        e.preventDefault();
        build_interests();
        $("#add-interest-form").val("");

        return false;
    });

    $('#logout-button').click(function () {
        Cookies.remove('user_secret');
    });
});