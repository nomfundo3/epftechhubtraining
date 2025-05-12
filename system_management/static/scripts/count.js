$(document).ready(function() {
    var duration = 500;
    var step = 1;
    var targetCount = parseInt($("#user_count").text());
    var currentCount = 0;
    $({ count: currentCount }).animate({
        count: targetCount
    }, {
        duration: duration,
        step: function() {
            $("#user_count").text(Math.floor(this.count));
        },
        complete: function() {
            $("#user_count").text(targetCount);
        }
    });
});