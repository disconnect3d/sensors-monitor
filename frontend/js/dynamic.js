
/*********************************
    Login form
**********************************/    
    
    var isLogged = false;               // Is user logged in?

    // Show login window
    function loginShow()
    {
        var loginForm = $("#loginMenu");

        if (findEnv() != "xs")
        {
            hideDim();
            loginForm.removeClass("loginMenuFull");
            loginForm.css("left", ($("#userLogin").offset().left - loginForm.width()) + "px");
            loginForm.css("top", ($("#navbar").offset().top + $("#navbar").height() - 1) + "px");   
        }
        else
        {
            showDim();
            loginForm.addClass("loginMenuFull");
        }

        $("#loginLogin").removeClass("inputInvalid");
        $("#loginPass").removeClass("inputInvalid");
        
        loginForm.css("display", "block");
        $("#loginLogin").focus();
    }

    // Handle click on login icon
    function loginShowClick(event)
    {
        event.stopPropagation();

        if (isLogged)
            logout();
        else
            loginShow();
    }

    // Adjust position of login window on resize
    function loginOnResize()
    {
        if ($("#loginMenu").is(':visible'))
            loginShow();
    }

    function loginHideStop(e)
    {
        e.stopPropagation();
    }
    
    // Hide login window
    function loginHide()
    {
        if ($("#loginMenu").css("display") != "none")
        {
            $("#loginMenu").css("display", "none");
            hideDim();
        }
    }
    
    // Invoke this function after receiving a confirmation that user has logged in
    function setLoggedIn()
    {
        isLogged = true;
        $("#userLogin").data("hint", "Click to log out.");
        $("#logOut").removeClass("template");
        loginHide();
    }

    // Invoke this function after receiving a confirmation that user has logged out
    function setLoggedOut()
    {
        isLogged = false;
        $("#userLogin").data("hint", "Click to log in.");
        $("#logOut").addClass("template");
    }

    // Function sends request to log in
    function login()
    {
        $("#loginLogin").trigger('input');
        $("#loginPass").trigger('input');

        if ($("#loginLogin").val() == "" || $("#loginPass").val() == "")
        {
            statusError("Fill both login and password.")
            return; 
        }

        // TODO - send proper AJAX request
        setLoggedIn();  // This should not be here (MOCK)
    }
    
    // Function sends request to log out
    function logout()
    {
        // TODO - send proper AJAX request
        setLoggedOut(); // This should not be here (MOCK)
    }




/*********************************
    Status
**********************************/    
    
    var statusHideHandle = null;            // Handle to timer that hides ok/error statuses.
    var statusOkError    = false;           // True if Ok or Error message is shown.

    // Helper function
    function status(text, type)
    {
        clearTimeout(statusHideHandle);

        $("#status").removeClass();
        $("#statusText").html(text);

        if (text != "")
        {
            $("#status").addClass("statusShow");
            $("#status").addClass(type);        
        }
    } 
    
    function statusInfo(text)
    {
        if (!statusOkError)
            status(text, "statusInfo");            
    }

    function statusOk(text)
    {
        status(text, "statusOk");       
        statusHideHandle = setTimeout(statusHide, 1600);
        statusOkError = true;
    }

    function statusError(text)
    {
        status(text, "statusError");        
        statusHideHandle = setTimeout(statusHide, 2000);
        statusOkError = true;
    }

    function statusHide()
    {
        statusOkError = false;
        $("#status").removeClass();
    }

    function statusHideInfo()
    {
        if (!statusOkError)
            statusHide();
    }






/*********************************
    Ask yes/no
**********************************/    
    
    var askActive  = false;                 // True when the ask window is visible
    var askHandler = null;                  // Handler function that is invoked when the user gives yes response
    var askObject  = null;                  // Object passed to the askHandler

    function askYesNo(question, handler, argument)
    {
        askActive  = true;
        askHandler = handler;
        askObject  = argument;

        $("#askMsg").html(question);
        $("#askWrapper").css("display", "flex");

        $("#askYes").focus();
    } 

    function askHideStop(e)
    {
        e.stopPropagation();
    }

    function askHide()
    {
        askActive  = false;
        askHandler = null;
        $("#askWrapper").css("display", "none");
    }

    function askAccept()
    {
        if (askHandler)
            askHandler(askObject);

        askHide();
    }
