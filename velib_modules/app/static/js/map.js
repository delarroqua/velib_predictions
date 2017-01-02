var map;
var bourdon = {lat: 48.847725125668795, lng: 2.365939153127159};

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: bourdon,
        zoom: 14
    });

    /*
    var marker = new google.maps.Marker({
      position: bourdon,
      map: map
    });
    */

    // var input = document.getElementById('txt-locations').value;

    var markers = [
        ['11043', 48.862650300140295, 2.367053490449912],
        ['11017', 48.854176040414856, 2.396093495321842]
    ];

    for (i = 0; i < markers.length; i++ ) {
        var position = new google.maps.LatLng(markers[i][1], markers[i][2]);
        marker = new google.maps.Marker({
            position: position,
            map: map,
            title: markers[i][0]
        }
    }
};


/*
var number, lat, lng;

number = markers[i][0];
        lat = markers[i][1];
        lng = markers[i][2];
        addMarkerToMap(map, number, lat, lng);

function addMarkerToMap(mapElement, number, lat, lng) {
    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(lat, lng),
        map: mapElement
    });
}

*/