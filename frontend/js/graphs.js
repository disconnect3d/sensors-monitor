
/*********************************
    Items
**********************************/    

    function grapItemClick(e)
    {
        $(e.target).closest(".grapItem").toggleClass("grapItemOn", 300);
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