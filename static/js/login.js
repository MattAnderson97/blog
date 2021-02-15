function toggleForm()
{
    $("#login-box").toggleClass("hidden");
    $("#overlay").toggleClass("hidden");
}

$(document).ready(function(){
    $("#login-button").click(toggleForm);
    $("#close-form-btn").click(toggleForm);

    $(document).keyup(function(event){
        if(event.which === 27 && !($("#form-box").hasClass("hidden")))
        {
            toggleForm();
        }
    });
});