$(document).ready(function(){
    $(document).on('click', '#monitorSelector li', function() {
        $('#monitorSelector li').removeClass('active');
        $(this).addClass('active');
    });

    $('#resources').DataTable();

});
