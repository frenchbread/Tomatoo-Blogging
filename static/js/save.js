function savee(post_id){
    $.get('/post/'+post_id+'/save', function(data) {

        $("#this_p"+post_id).html('<a href="javascript:void(0);" class="btn btn-warning btn-xs" style="float:right" onclick="removee('+ post_id +')" ><span class="glyphicon glyphicon-star"></span> Saved </a>');

    });
    return false
}

function removee(post_id){
    $.get('/post/'+post_id+'/remove', function(data) {

        $("#this_p"+post_id).html('<a href="javascript:void(0);" class="btn btn-primary btn-xs" style="float:right" onclick="savee('+ post_id +')" ><span class="glyphicon glyphicon-star-empty"></span> Save for later </a>');


        /*setTimeout(function(){
            ui.notify(data)
                .effect('slide');
        });*/

    });
    return false
}