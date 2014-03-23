//Executes your code when the DOM is ready.  Acts the same as $(document).ready().
$(function() {
  //Calls the selectBoxIt method on your HTML select box.
  $("select").selectBoxIt();
});



$('#morelegs').hide();
    
//reveal morelegs div
$('.morelegs').click(function(e) {
    e.stopPropagation();
    e.preventDefault();
    $("#morelegs").show();
    $('.morelegs').hide();
    }); 
    
$('.lesslegs').click(function(e) {
    e.stopPropagation();
    e.preventDefault();
    $("#morelegs").hide();
    $('.morelegs').show();
    });     

$('#morelegsagain').hide();
    
//reveal morelegs div
$('.morelegsagain').click(function(e) {
    e.stopPropagation();
    e.preventDefault();
    $("#morelegsagain").show();
    $('.lesslegs').hide();
    $('.morelegsagain').hide();
    }); 
    
$('.lesslegsagain').click(function(e) {
    e.stopPropagation();
    e.preventDefault();
    $("#morelegsagain").hide();
    
    $('.lesslegs').show();
    $('.morelegsagain').show();
    });  
    
$('#morelegsaway').hide();
    
//reveal morelegs div
$('.morelegsaway').click(function(e) {
    e.stopPropagation();
    e.preventDefault();
    $("#morelegsaway").show();
    $('.morelegsaway').hide();
    }); 
    
$('.lesslegsaway').click(function(e) {
    e.stopPropagation();
    e.preventDefault();
    $("#morelegsaway").hide();
    $('.morelegsaway').show();
    });     

$('#morelegsagainaway').hide();
    
//reveal morelegs div
$('.morelegsagainaway').click(function(e) {
    e.stopPropagation();
    e.preventDefault();
    $("#morelegsagainaway").show();
    $('.lesslegsaway').hide();
    $('.morelegsagainaway').hide();
    }); 
    
$('.lesslegsagainaway').click(function(e) {
    e.stopPropagation();
    e.preventDefault();
    $("#morelegsagainaway").hide();
    
    $('.lesslegsaway').show();
    $('.morelegsagainaway').show();
    });  
    

///////

$('#morelegsN').hide();
    
//reveal morelegs div
$('.morelegsN').click(function(e) {
    e.stopPropagation();
    e.preventDefault();
    $("#morelegsN").show();
    $('.morelegsN').hide();
    }); 
    
$('.lesslegsN').click(function(e) {
    e.stopPropagation();
    e.preventDefault();
    $("#morelegsN").hide();
    $('.morelegsN').show();
    });     

$('#morelegsagainN').hide();
    
//reveal morelegs div
$('.morelegsagainN').click(function(e) {
    e.stopPropagation();
    e.preventDefault();
    $("#morelegsagainN").show();
    $('.lesslegsN').hide();
    $('.morelegsagainN').hide();
    }); 
    
$('.lesslegsagainN').click(function(e) {
    e.stopPropagation();
    e.preventDefault();
    $("#morelegsagainN").hide();
    
    $('.lesslegsN').show();
    $('.morelegsagainN').show();
    });  
    
$('#morelegsawayN').hide();
    
//reveal morelegs div
$('.morelegsawayN').click(function(e) {
    e.stopPropagation();
    e.preventDefault();
    $("#morelegsawayN").show();
    $('.morelegsawayN').hide();
    }); 
    
$('.lesslegsawayN').click(function(e) {
    e.stopPropagation();
    e.preventDefault();
    $("#morelegsawayN").hide();
    $('.morelegsawayN').show();
    });     

$('#morelegsagainawayN').hide();
    
//reveal morelegs div
$('.morelegsagainawayN').click(function(e) {
    e.stopPropagation();
    e.preventDefault();
    $("#morelegsagainawayN").show();
    $('.lesslegsawayN').hide();
    $('.morelegsagainawayN').hide();
    }); 
    
$('.lesslegsagainawayN').click(function(e) {
    e.stopPropagation();
    e.preventDefault();
    $("#morelegsagainawayN").hide();
    
    $('.lesslegsawayN').show();
    $('.morelegsagainawayN').show();
    });









//////





    


$("#AwayWRNo").hide();

         
    $(function() {
    $types1 = $('.AwayWR');
    $away1 = $('#AwayWRNo');
    $types1.change(function() {
        $this = $(this).val();
        if ($this == "AwayWRNo") {
            $away1.show(500);
                    }
        else  {
            $away1.hide(250);
        }
    });
});    

$("#ToNormNo").hide();
 
    $(function() {
    $types2 = $('.ToNorm');
    $away2 = $('#ToNormNo');
    $types2.change(function() {
        $this = $(this).val();
        if ($this == "ToNormNo") {
            $away2.show(500);
                    }
        else  {
            $away2.hide(250);
        }
    });
});   


$("#AwayNormNo").hide();
 
    $(function() {
    $types = $('.AwayNorm');
    $away = $('#AwayNormNo');
    $types.change(function() {
        $this = $(this).val();
        if ($this == "AwayNormNo") {
            $away.show(500);
                    }
        else  {
            $away.hide(250);
        }
    });
});   
