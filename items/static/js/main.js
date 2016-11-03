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

function getCableLength( lengths ) {

    $( '#id_cable_type' ).change( function(event) {
        var cable_type = $( this ).val();
        $( '#id_length' ).val( lengths[ cable_type ] );
    });
}

function getBCableLength() {

    var lengths = ["3008", "3008", "3024", "3130", "3160"];

    getCableLength( lengths );
}

function getHCableLength() {

    var lengths = ["1500", "2250", "1500", "2250", "1140", "1500",
                   "1534", "1534", "1540"];

    getCableLength( lengths );
}



$(document).ready( function() {

    if ($(location).attr('pathname') == '/product/create_std_cable/') {
        showChecker();
    }

    if ($(location).attr('pathname') == '/product/create_b_cable/') {
        getBCableLength();
    }

    if ($(location).attr('pathname') == '/product/create_h_cable/') {
        getHCableLength();
    }
});