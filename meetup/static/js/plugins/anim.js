$(document).ready(function() {

    
    $( ".menu-mob .menu" ).click(function() {
        $(".lighMenu").fadeIn(500);
        $(".lighMenu .izq").animate({"left":"0px"});
    });
    
    $( ".lighMenu .izq .cerrar" ).click(function() {
        $(".lighMenu").fadeOut(500);
        $(".lighMenu .izq").animate({"left":"-300px"});
    });
    
    $( ".lighMenu .der" ).click(function() {
        $(".lighMenu").fadeOut(500);
        $(".lighMenu .izq").animate({"left":"-300px"});
    });

    $( ".description .open" ).click(function() {
        $(".description .hidden-text").slideDown();
        $(".description .open").hide(10);
        $(".description .close").fadeIn(500);
    });

    $( ".description .close" ).click(function() {
        $(".description .hidden-text").slideUp();
        $(".description .open").fadeIn(500);
        $(".description .close").hide(10);
    });


    /*$( ".titleMobile" ).click(function() {
        $(".side-column").animate({"left":"0%"});
    });

    $( ".close-side" ).click(function() {
        $(".side-column").animate({"left":"-100%"});
    });*/

    /*if($(".titleMobile").is(":visible") == false){
        $(".side-column").animate({"left":"0%"});
    }
    else{
        $(".side-column").animate({"left":"-100%"});
    }*/

});





