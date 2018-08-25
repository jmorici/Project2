

var myMap = L.map('map', {
  center: [37.09, -95.71],
  zoom: 4
});


// Adding tile layer
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
  maxZoom: 18,
  id: 'mapbox.light',
  accessToken: API_KEY
}).addTo(myMap);

var newtry = "/firedata"

// Function to determine marker color based on earthquake magnitude
var colors = ["#7FFF00", "#dfedbe", "#eede9f", "#FF8C00", "#FA8072", "#FF0000", "#F312E9"]
function fillColor(newtry) {
  var Class = newtry.Class;

  // console.log(Class);

  if (Class == "A") {
    return colors[0]
  }
  else if (Class == "B") {
    return colors[1]
  }
  else if (Class == "C") {
    return colors[2]
  }
  else if (Class == "D") {
    return colors[3]
  }
  else if (Class == "E") {
    return colors[4]
  }
  else if (Class == "G") {
    return colors[5]
  }
  else {
    return colors[6]
  }
}


d3.json(newtry, function(data){

  console.log(data);

// An array which will be used to store created cityMarkers
  var fireMarkers = [];
  for (var i = 0; i < data.length; i++) {
    var location = data[i];
    
    if (location) {
      L.circle([location.latitude, location.longitude], {
        radius: 20,
        stroke: false,
        // radius: (data[i].Size),
        // radius: markerSize(data),
        // fillColor: ("#FFCC33"),
        fillColor: fillColor(data[i]),
        weight: 10,
        opacity: 5,
        fillOpacity: 2
        
  
    }).bindPopup(location.Cause).addTo(myMap);

    }
  }

   
});