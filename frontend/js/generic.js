/*********************************
 Generic functions
 **********************************/

// Find environment (screen resolution)
function findEnv() {
    var envs = ['xs', 'sm', 'md', 'lg'];

    var $el = $('<div>');
    $el.appendTo($('body'));

    for (var i = envs.length - 1; i >= 0; i--) {
        var env = envs[i];

        $el.addClass('hidden-' + env);
        if ($el.is(':hidden')) {
            $el.remove();
            return env;
        }
    }
}

function showDim() {
    $("#dim").css("display", "block");
}

function hideDim() {
    $("#dim").css("display", "none");
}

function makeAjaxCall(login, pass, hostname, monitorName, monitorId) {
    var headers = null;

    if ( login && password) {
        headers = {
            'Authorization': 'Basic ' + btoa(login + ':' + pass)
        };
    }

    $.ajax({
        url: hostname,
        xhrFields: {
            withCredentials: true
        },
        headers: headers,
        crossDomain: true,
        type: "GET",
        dataType: "json",
    })
    .done(function (data) {
        addMonitor(monitorName, monitorId);
        $.each(data, function (i, obj) {
            var key = obj.kind.kind_name;

            $.ajax({
                url: hostname + obj.id + "/measurements/",
                type: "GET",
                dataType: "json",
            }).done(function (data) {
                if (data.length >0)
                    addSensors(monitorId, monitorName, $('#monitorUrl').val(), obj.id, obj.kind.kind_name, data[data.length - 1].value);
                else
                    addSensors(monitorId, monitorName, $('#monitorUrl').val(), obj.id, obj.kind.kind_name, "No records");
            }).fail(function (xhr, status, errorThrown) {
                addSensors(monitorId, monitorName, obj.id, "Test sensor", "default");
            });



        });
    })
    .fail(function (xhr, status, errorThrown) {
        alert("Wrong url, login or password, try again!");
        console.log("Error: " + errorThrown);
        console.log("Status: " + status);
        console.dir(xhr);
    })
}


/*********************************
 Events
 **********************************/

function setupEvents() {
    // Generic:

    // Validate inputs (done in JS instead of CSS, so it validates only after first input change)
    $("input").on('input', function () {
        if ($(this).data('required')) {
            if ($(this).val() == "")
                $(this).addClass("inputInvalid");
            else
                $(this).removeClass("inputInvalid");
        }
    });


    // Hints
    $(document.body).on('mouseenter', '[data-hint]', function () {
        statusInfo($(this).data('hint'))
    });

    $(document.body).on('mouseleave', '[data-hint]', function () {
        statusHideInfo();
    });


    // Navigation
    $(".navLink").click(function () {
        loadSlide($(this).data("index"));
    });


    // Specific:
    // Login:
    $("#userLogin").click(loginShowClick);
    $("#loginMenu").click(loginHideStop);
    $("#loginButton").click(login);

        // Login:
    $("#addMonitor").click(addMonitorShowClick);
    $("#monitorMenu").click(loginHideStop);
    $("#addMonitorButton").off('click').on('click',addMonitorClick);


    // Ask yes/no
    $("#askWrapper").click(askHide);
    $("#askWindow").click(askHideStop);
    $("#askYes").click(askAccept);
    $("#askNo").click(askHide);

    // Resize
    windowResize();
}

function setupMeasEvents() {
    $("#measButGrid").click(measShowGrid);
    $("#measButList").click(measShowList);
    $("#measButSimple").click(measShowSimple);
    $("#measButDetail").click(measShowDetail);
    $("#measButSelect").click(measSelectAll);
    $("#measButDeselect").click(measDeselectAll);

    $("#measSearch").on('change keyup paste', measSearchResources);

    $("#measItems").on('click', '.measItem', function (e) {
        //alert("measitem");
        measToggleView(e);
    });

    $("#measItems").on('click', '.measAdd', function (e) {
        if (compSelectionActive){
            var res = $(this).attr("data-monitor-name");
            var sensor = $(this).attr("data-sensor-id");
            var url = $(this).attr("data-monitor-url");
            $('#compSelected').text(res + "::" + sensor).attr('data-sensor-id', sensor).attr('data-sensor-url', url);
            loadSlide(1);
            compSelectionActive = false;
        } else {
            measAdd(e);
            $('#grapPanel').children('.grapItem').remove();

            $('#measItems').find('.measSelected').each(function () {
                $('#grapPanel').append(
                    '<div class="grapItem" data-id="' + $(this).attr("data-sensor-id") + '" data-hint="Click to show / hide this measurement from graph">' +
                    '<div class="grapItemRes">' + $(this).attr("data-monitor-name") + ' :: </div>' +
                    '<div class="grapItemMeas">' + $(this).find(".measResName").text() + '</div>' +
                    '</div>'
                );
            });
        }
    });


    $("#measCancelComplex").click(measCancelComplex);

    setupEvents();
}

function setupCompEvents() {
    $("#compSelect").click(compSelectClick);

    $("#compAdd").click(compAddClick);


    $('#complexFrom').datetimepicker({format: 'yyyy-mm-dd hh:ii'});

    $('#complexTo').datetimepicker({format: 'yyyy-mm-dd hh:ii'});

    setupEvents();
}


function setupGrapEvents() {

    $("#grapPanel").on('click', '.grapItem', grapItemClick);

    // Date picker
    grapSetUpPickers();

    setupEvents();
}

function onSlideLoad(anchorLink, index, slideAnchor, slideIndex) {
    $(".navLink").removeClass("navActive");

    if (slideIndex == 0) {
        document.title = "Resources - Sensors Monitor";
        $("#nav0").addClass("navActive");
    }
    else if (slideIndex == 1) {
        document.title = "Complex measurements - Sensors Monitor";
        $("#nav1").addClass("navActive");
    }
    if (slideIndex == 2) {
        document.title = "Graphs - Sensors Monitor";
        $("#nav2").addClass("navActive");
    }
}

function loadSlide(index) {
    $.fn.fullpage.moveTo(1, index);
}

function windowResize() {
    loginOnResize();
    measOnResize();
}


/*********************************
 Document handlers
 **********************************/

// When document loads
$(document).ready(function () {

    // Load layouts and init events
    setupEvents();

    $("#secMeasurements").load("layout/meas.html", setupMeasEvents);
    $("#secComplex").load("layout/complex.html", setupCompEvents);
    $("#secGraphs").load("layout/graphs.html", setupGrapEvents);


    // Init scrolling sections
    $('#contentMain').fullpage(
        {
            lockAnchors: false,
            keyboardScrolling: true,
            controlArrows: false,

            afterSlideLoad: onSlideLoad
        });

    //makeAjaxCall("http://disconnect3d.pl:1337/sensors/", "Monitor 1", "m1");

    // Initial
    loadSlide(0);
    measShowGrid();
    measShowSimple();

    // Initial resize
    windowResize();

    $('body').css('overflow', 'auto');
});

// When resolution/size changes
$(window).resize(function () {
    windowResize();
});

// Used to hide elements
$(document).click(function () {
    loginHide();
    monitorHide();
});

// Used as a way to answer to yes/no window
$(document).keyup(function (e) {
    if (askActive && e.keyCode === 27)  // Escape pressed
        askHide();
});