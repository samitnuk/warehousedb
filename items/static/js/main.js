function showChecker() {
    $('#id_travel').change( function(event) {
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


$(document).ready( function() {
    showChecker();
});