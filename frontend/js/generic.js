
/*********************************
    Generic functions
**********************************/    

    // Find environment (screen resolution)
    function findEnv() 
    {
        var envs = ['xs', 'sm', 'md', 'lg'];

        var $el = $('<div>');
        $el.appendTo($('body'));

        for (var i = envs.length - 1; i >= 0; i--) {
            var env = envs[i];

            $el.addClass('hidden-'+env);
            if ($el.is(':hidden')) {
                $el.remove();
                return env;
            }
        }
    }

    function showDim()
    {
        $("#dim").css("display", "block");
    }
    
    function hideDim()
    {
        $("#dim").css("display", "none");
    }



/*********************************
    Events
**********************************/    

    function setupEvents()
    {
        // Generic: 

        // Validate inputs (done in JS instead of CSS, so it validates only after first input change)
        $("input").on('input', function() 
        {
            if($(this).data('required'))
            {
                if ($(this).val() == "")
                    $(this).addClass("inputInvalid");
                else
                    $(this).removeClass("inputInvalid");
            }
        });


        // Hints
        $('[data-hint]').hover(function() 
        {
            statusInfo($(this).data('hint'));
        },
        statusHideInfo); 


        // Navigation
        $(".navLink").click(function()
        {
            loadSlide($(this).data("index"));
        });


        // Specific:
            // Login:
            $("#userLogin").click(loginShowClick);
            $("#loginMenu").click(loginHideStop);
            $("#loginButton").click(login);

            // Ask yes/no
            $("#askWrapper").click(askHide);
            $("#askWindow").click(askHideStop);
            $("#askYes").click(askAccept);
            $("#askNo").click(askHide);

        // Resize
            windowResize();
    }
        
    function setupMeasEvents()
    {
        $("#measButGrid").click(measShowGrid);         
        $("#measButList").click(measShowList);         
        $("#measButSimple").click(measShowSimple);         
        $("#measButDetail").click(measShowDetail);         
        $("#measButSelect").click(measSelectAll);         
        $("#measButDeselect").click(measDeselectAll);         

        $(".measItem").click(measToggleView);         
        $(".measAdd").click(measAdd);                    

        $("#measCancelComplex").click(measCancelComplex);      

        setupEvents();              
    }

    function setupCompEvents()
    {
        $("#compSelect").click(compSelectClick);

        // Init time pickers
        $("#compWindow").timeDurationPicker(
            {
                onSelect: compWindowSecSelect,
                seconds: true,
                years: false
            });

        $("#compInter").timeDurationPicker(
            {
                onSelect: compInterSecSelect,
                seconds: true,
                years: false
            });

        setupEvents();
    }



    function setupGrapEvents()
    {
        $(".grapItem").click(grapItemClick);

        // Date picker
        grapSetUpPickers();

        setupEvents();
    }

    function onSlideLoad(anchorLink, index, slideAnchor, slideIndex)
    {
        $(".navLink").removeClass("navActive");

        if (slideIndex == 0)
        {
            document.title = "Resources - Sensors Monitor";
            $("#nav0").addClass("navActive");
        }
        else
        if (slideIndex == 1)
        {
            document.title = "Complex measurements - Sensors Monitor";
            $("#nav1").addClass("navActive");   
        }
        if (slideIndex == 2)
        {
            document.title = "Graphs - Sensors Monitor";
            $("#nav2").addClass("navActive");
        }
    } 

    function loadSlide(index)
    {
        $.fn.fullpage.moveTo(1, index);
    }

    function windowResize()
    {
        loginOnResize();
        measOnResize();
    }


/*********************************
    Document handlers
**********************************/    

    // When document loads
    $(document).ready(function()
    {
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

        // Initial        
        loadSlide(0);
        measShowGrid();
        measShowSimple();

        // Initial resize
        windowResize();
    });

    // When resolution/size changes
    $(window).resize(function() 
    {
        windowResize();
    });

    // Used to hide elements
    $(document).click(function() 
    {
        loginHide();            
    });

    // Used as a way to answer to yes/no window
    $(document).keyup(function(e) 
    {
        if (askActive && e.keyCode === 27)  // Escape pressed
            askHide();
    });