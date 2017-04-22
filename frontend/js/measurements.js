
/*********************************
 Generic
**********************************/

    // Invoked on resize
    function measOnResize()
    {
        $("#secMeasurements").css("height", ($("#contentMain").height() -  $("#measPanel").height() - 60) + "px");
    }


/*********************************
    Control panel buttons
**********************************/

    // Switch view to grid
    function measShowGrid()
    {
        $("#measButGrid").addClass("buttonMinOn");
        $("#measButList").removeClass("buttonMinOn");

        $("#measItems").removeClass();
        $("#measItems").addClass("measGridView");
    }

    // Switch view to list
    function measShowList() 
    {
        
        $("#measButGrid").removeClass("buttonMinOn");
        $("#measButList").addClass("buttonMinOn");

        $("#measItems").removeClass();
        $("#measItems").addClass("measListView");
    }


    // Switch to simplified view
    function measShowSimple() 
    {
        $("#measButSimple").addClass("buttonMinOn");
        $("#measButDetail").removeClass("buttonMinOn");

        $(".measItem").removeClass("measDetail", 500);
    }

    // Switch to detailed view
    function measShowDetail() 
    {
        $("#measButSimple").removeClass("buttonMinOn");
        $("#measButDetail").addClass("buttonMinOn");

        $(".measItem").addClass("measDetail", 500);
    }

    // Toggle individual resource between simplified and detailed view
    function measToggleView(e)
    {
        $(e.target).closest(".measItem").toggleClass("measDetail", 500);
    }


    // Select all measurements
    function measSelectAll()
    {
        $(".measAdd").addClass("measSelected");
    }

    // Deselect all measurements
    function measDeselectAll()
    {
        $(".measAdd").removeClass("measSelected");
    }

    // Add selected measurement to graph view
    function measAdd(e)
    {
        e.stopPropagation();

        $(e.target).closest(".measAdd").toggleClass("measSelected");
    }


    function measCancelComplex()
    {
        compSelectionActive = false;
        $("#measSelectComplex").addClass("template");
    }

        
