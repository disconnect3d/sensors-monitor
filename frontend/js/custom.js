$(document).ready(function(){
    $(document).on('click', '#monitorSelector li', function() {
        $('#monitorSelector li').removeClass('active');
        $(this).addClass('active');
    });

    if ( $('#resources').length ){
        $('#resources').DataTable();
    }

});