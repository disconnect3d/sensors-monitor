
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
        alert(compWindowSec);
        alert(compInterSec);
    }