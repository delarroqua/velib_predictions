var map;
var bourdon = {lat: 48.847725125668795, lng: 2.365939153127159};


function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: bourdon,
        zoom: 14
    });

    var bounds = new google.maps.LatLngBounds();
    var infoWindow = new google.maps.InfoWindow(), marker, i;

    // Loop through our array of markers & place each one on the map
    for( i = 0; i < list_stations.length; i++ ) {
        var position = new google.maps.LatLng(list_stations[i][3], list_stations[i][4]);
        bounds.extend(position);
        marker = new google.maps.Marker({
            position: position,
            map: map,
            title: String(list_stations[i][0])
        });

        // Allow each marker to have an info window
        google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
                infoWindow.setContent(
                '<h4>' + 'Station n°' + String(list_stations[i][0]) + '</h4>'
                + '<h5>' + String(list_stations[i][1]) + '</h5>'
                + '<h5>' + String(list_stations[i][2]) + '</h5>'
                + '<h5>' + 'Nombre de support de vélo: ' + String(list_stations[i][5]) + '</h5>'
                );
                infoWindow.open(map, marker);
                $('#number_station').val(this.title)
            }
        })(marker, i));

        // Automatically center the map fitting all markers on the screen
        // map.fitBounds(bounds);
    };
};


