
/*********************************
    Time pickers & UI
**********************************/    

    var compWindowSec = 0;
    var compInterSec = 0;

    function compWindowSecSelect(element, seconds, humanDuration)
    {
        $('#compWindow').val(humanDuration);
        compWindowSec = seconds;
    }

    function compInterSecSelect(element, seconds, humanDuration)
    {
        $('#compInter').val(humanDuration);
        compInterSec = seconds;
    }

    function compReset()
    {

    }


/*********************************
    Selection of a measurement
**********************************/    

    var compSelectionActive = false;

    function compSelectClick()
    {
        compSelectionActive = true;
        $("#measSelectComplex").removeClass("template");
        loadSlide(0);
    }

    function compAddClick()
    {
        var headers = null;

        var login = $('#loginLogin').val();
        var pass = $('#loginPass').val();

        if ( login && pass) {
            headers = {
                'Authorization': 'Basic ' + btoa(login + ':' + pass)
            };
        } else {
            statusError('You have to be logged in.');
        }
        var sensorId = $('#compSelected').attr('data-sensor-id');
        var url = $('#compSelected').attr('data-sensor-url');

        $.ajax({
            url: url + "/sensors/"+sensorId+"/complex-measurements/",
            xhrFields: {
                withCredentials: true
            },
            headers: headers,
            crossDomain: true,
            type: "POST",
            dataType: "json",
            data: {
                name: $('#compName').val(),
                begin: $('#complexFrom').val(),
                end: $('#complexTo').val(),
                time_window: $('#compFrame').val(),
                frequency: $('#compInter').val()
            }
        })
        .done(function (data) {

        })
        .fail(function (xhr, status, errorThrown) {
            alert("Wrong url, login or password, try again!");
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
        })
    }