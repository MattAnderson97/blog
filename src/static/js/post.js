$('#commentsToggle').click(() => {
    $("#commentsBar").toggleClass("hidden");
});

$('#closeCommentsBtn').click(() => {
    if (!$("#commentsBar").hasClass("hidden"))
    {
        $("#commentsBar").addClass("hidden");
    }
})