// enable tooltips from bootstrap
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
});


let sidebar = $('.sidebar');
let sidebar_btn = $('#sidebar-btn');
let sidebar_btn_icon = $("#sidebar-btn-icon")

let replace_class = function(element, old_class, new_class)
{
    element.removeClass(old_class);
    element.addClass(new_class);
}


let toggle_sidebar = function()
{    
    // expand/shrink sidebar
    sidebar.toggleClass('active');

    if (sidebar.hasClass('active'))
    {
        // change the icon of the sidebar button to a cross
        replace_class(sidebar_btn_icon, 'bi-list', 'bi-x');
        // disable tooltips
        $('.sidebar-item').tooltip('disable');
    }
    else
    {
        // change the icon of the sidebar button to a list
        replace_class(sidebar_btn_icon, 'bi-x', 'bi-list');
        // allow tooltips
        $('.sidebar-item').tooltip('enable');
    }
}

let hide_sidebar = function()
{    
    // ensure sidebar is active
    if (sidebar.hasClass('active'))
    {
        // remove active class from sidebar to make it shrink
        sidebar.removeClass('active');
        // change the icon of the sidebar button to a list
        replace_class(sidebar_btn_icon, 'bi-x', 'bi-list');
        // allow tooltips
        $('.sidebar-item').tooltip('enable');
    }
}

sidebar_btn.click(toggle_sidebar);
// $('.content').click(hide_sidebar);

// $('#roles_link').click(function(){
//     $('#panel').load('/roles');
// });

// $('#users_link').click(function(){
//     $('#panel').load('/users/manage');
// });