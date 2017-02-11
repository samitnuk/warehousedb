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

function showCategoryFields() {
    $( '.category' ).click( function() {
        table = $( this ).next();
        table.toggle();
    });
}

function getDatePicker() {
    var languageUA = {
        days: ['Неділя','Понеділок','Вівторок','Середа','Четвер','Пятниця','Субота'],
        daysShort: ['Нед','Пон','Вів','Сер','Чет','Пят','Суб'],
        daysMin: ['Нд','Пн','Вт','Ср','Чт','Пт','Сб'],
        months: ['Січень','Лютий','Березень','Квітень','Травень','Червень','Липень','Серпень','Вересень','Жовтень','Листопад','Грудень'],
        monthsShort: ['Січ','Лют','Бер','Кві','Тра','Чер','Лип','Сер','Вер','Жов','Лис','Гру'],
        today: 'Сьогодні',
        clear: 'Очистити',
        dateFormat: 'yyyy-mm-dd',
        timeFormat: 'hh:ii',
        firstDay: 1,
    };
    $('#id_range_start').datepicker({
        language: languageUA,
        maxDate: new Date(),
    });
    $('#id_range_stop').datepicker({
        language: languageUA,
        maxDate: new Date(),
    });
}

$(document).ready( function() {
    if ($( "form" ).hasClass( "std-cable" )) { showChecker(); }
    if ($( "form" ).hasClass( "b-cable" )) { getBCableLength(); }
    if ($( "form" ).hasClass( "h-cable" )) { getHCableLength(); }
    if ($( "form" ).hasClass( "toggle-categories" )) { showCategoryFields(); }
    if ($( "form" ).hasClass( "date-range" )) { getDatePicker(); }
});
