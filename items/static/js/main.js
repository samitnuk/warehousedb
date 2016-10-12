function showChecker() {
    $( '#id_travel' ).change( function(event) {
        var travel = $( this ).val();
        if ( travel == 3 ) {
            $( '.hidden_at_start' ).show()
        } else {
            $( '#id_is_plastic_sleeves' ).prop( 'checked', false );
            $( '.hidden_at_start' ).hide()
        }
        return true;
    });
}

function getBCableLength() {

    var lengths = ["3008", "3008", "3024", "3130", "3160"]

    $( '#id_cable_type' ).change( function(event) {
        var cable_type = $( this ).val();
        $( '#id_length' ).val( lengths[ cable_type ] );
    });
}


$(document).ready( function() {
    showChecker();
    getBCableLength();
});