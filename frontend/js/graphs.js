var hostname = "http://disconnect3d.pl:1337/sensors/";

/*********************************
    Items
**********************************/    

    function grapItemClick(e)
    {
        $('#grapPanel').find('.grapItem').removeClass("grapItemOn");
        $(e.target).closest(".grapItem").toggleClass("grapItemOn", 300);
            $.ajax({
            url: hostname + $(e.target).closest('.grapItem').attr('data-id') + "/measurements",
            crossDomain: true,
            type: "GET",
            dataType: "json",
        }).done(function (data) {
            var graphData = [];
            for (var i = 0; i < data.length; i++) {
                graphData.push([new Date(data[i].measurement_time).getTime(), data[i].value]);
            }
            console.log(graphData);
            $.plot($("#graph"), [graphData], {xaxis: { mode: "time" }} );
        });
    }

    function grapGetDate(element)
    {
        var date;

        try
        {
            date = $.datepicker.parseDate( "dd/mm/yy", element.value );
        } catch( error )
        {
            date = null;
        }

        return date;
    }

    var grapDateFrom = null;
    var grapDateTo   = null;

    function grapSetUpPickers(element)
    {
        // API documentation: http://api.jqueryui.com/datepicker/

        grapDateFrom = $( "#grapDateFrom" ).datepicker
        ({
            defaultDate: "+1w",
            changeMonth: true,
            changeYear: true,
            firstDay: 1,
            dateFormat: "dd/mm/yy",
            numberOfMonths: 1
        })
        .on( "change", function()
        {
            grapDateTo.datepicker( "option", "minDate", grapGetDate( this ) );
        });

        grapDateTo = $( "#grapDateTo" ).datepicker
        ({
            defaultDate: "+1w",
            changeMonth: true,
            changeYear: true,
            firstDay: 1,
            dateFormat: "dd/mm/yy",
            numberOfMonths: 1
        })
        .on( "change", function()
        {
            grapDateFrom.datepicker( "option", "maxDate", grapGetDate( this ) );
        });
    }