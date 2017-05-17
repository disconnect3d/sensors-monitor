/*********************************
 Dynamic (Ajax response) based context
**********************************/


function addMonitor(){
    alert("Add monitor");
    var monitorDiv = "<div class='measItem measSimpleView' data-hint='Click to toggle between simplified and detailed view.'>" +
        "<div class='measHeader'>" +
            "<div class='measItemName'>" +
                "Default Monitor" +
            "</div>" +
        "</div>" +
        "<div class='measItemRessMain'>" +
            "<div class='measItemRess' id='hostname'></div></div></div>";

    $("#measItems").append(monitorDiv);
}

function addSensors(monitorID) {
    var singleSensorDiv = "<div class='measItemRes measAdd'>" +
                    "<i class='fa fa-thermometer-full' data-hint='Select (deselect) this measurement to the graph view.'></i>" +
                    "<div class='measResDet'> <span class='measResName'>key</span> <span class='measResValue'>value</span></div></div>";
    $("#" + monitorID).append(singleSensorDiv);
}






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
        $(".measItem").each(function(){
           if (!$(this).hasClass("template")){
               $(this).find(".measAdd").addClass("measSelected")
           }
        });
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

    // Search bar filter functionality
    function measSearchResources()
    {
        var value = $(this).val();
        $(".measItem").each(function(){
            if (($(this).find(".measItemName").text().indexOf(value) >=0) || ($(this).find(".measResName").text().indexOf(value) >=0) ){
                $(this).removeClass("template");
            } else {
                $(this).addClass("template");
            }
        });
    }

        
