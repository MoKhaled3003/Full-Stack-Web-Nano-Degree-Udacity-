var map;
var defaultIcon;
var highlightedIcon;
var markers = [];
var MosqueApi;
var mosques = [];


//function to initialize map
function initMap() {
	"use strict";
	var styles;
	map = new google.maps.Map(document.getElementById('map'), {
		center: new google.maps.LatLng(30.037788,31.29393),
		zoom: 13,
		styles: styles,
		mapTypeControl: false
	});


	MosqueApi = new AppViewModel();
	ko.applyBindings(MosqueApi);

 //parsing filter to be a string to apply toLowerCase function on it
 //if this string.prototype wasn't applied it will cause an type error
 //ko.utils function
	String.prototype.filter = function(other) {
	return this.indexOf(other) !== -1;
};


}

//this function will be excuted if there is a failure in the get request
//that makes loading map fail
function googleError() {
    //self.abc = ko.observable('');
    $('#query-summary').text("Could not load Google Maps");
    $('#ulist').hide();
}

//knockout's ViewModel
function AppViewModel() {
	google.maps.event.addDomListener(window, 'load', foursquareApiMosques);
	var self = this;
	self.mosqueListItems = ko.observableArray([]);
	self.filter = ko.observable('');
	self.latLng = ko.observable('30.037788,31.29393');
	var infoWindow = new google.maps.InfoWindow();
	self.queryResult = ko.observable('');

	self.filteredMosques = ko.pureComputed(function () {
//set markers of mosques to null as an intialization
		self.mosqueListItems().forEach(function(mosque) {
			mosque.marker.setMap(null);
		});

//ko.utlis have a usefull knockout functions
//http://www.knockmeout.net/2011/04/utility-functions-in-knockoutjs.html

//var filter = self.filter().toLowerCase();
		var results = ko.utils.arrayFilter(self.mosqueListItems(), function (mosque) {
			return mosque.name.toLowerCase().filter(self.filter().toLowerCase());
	//		return ko.utils.stringStartsWith(mosque.name.toLowerCase(), filter);

        });
		markers = [];
		results.forEach(function(mosque) {
			mosque.marker.setMap(map);
			markers.push(mosque.marker);
		});
		return results;
});

//function excuted when user clicks a mosque from the list
	    self.selectMosque = function (mosque) {
	        infoWindow.setContent(mosque.formattedInfoWindowData());
	        infoWindow.open(map, mosque.marker);
	        map.panTo(mosque.marker.position);
	        mosque.marker.setAnimation(google.maps.Animation.BOUNCE);
	        self.mosqueListItems().forEach(function (unselected_mosque) {
	            if (mosque != unselected_mosque) {
	                unselected_mosque.marker.setAnimation(null);
	            }
	        });
	    };

	function foursquareApiMosques() {
	// load foursquare api
	//you can find alot of search venues and interesting parameters at
	//https://developer.foursquare.com/docs/venues/search
	var url = "https://api.foursquare.com/v2/venues/search";
	var param = $.param({
		'v': "20131016",
		'client_id': "DDBW3LK4Q3SJOQ05RWELVUDZONIYYA1ZJHEYGMOTGQGF11XS",
		'client_secret': "3EYS5JPJOYSYOVYKC0M4BE0BHFJL0RIZMNLREQTS3AJM4LJU",
		'll': self.latLng(),
		'query': "mosque",
		'intent': "checkin",
		'radius': 2500
	});

	var data;
	$.ajax({
		url: url,
		data: param,
		dataType: 'json',
		async: true,
	}).done(function(response) {
		data = response.response.venues;
		data.forEach(function(mosque) {
			mosque = new MosqueFourSquareModel(mosque);
			mosques.push(mosque);
		});
		self.mosqueListItems(mosques);
		self.mosqueListItems().forEach(function(mosque) {
			if (mosque.map_latLng()) {
				google.maps.event.addListener(mosque.marker, 'click', function() {
					self.selectMosque(mosque);
				});
			}
		});
	}).fail(function (response, status, error) {
            $('#query-summary').text('Mosques info not loaded...');
        });
 }
 }

 var MosqueFourSquareModel = function(mosque, map) {
 	var self = this;
 	self.name = mosque.name;
 	self.lat = mosque.location.lat;
 	self.lng = mosque.location.lng;
	self.formattedAddress = mosque.location.formattedAddress;
 	self.checkinsCount = mosque.stats.checkinsCount;

 	self.map_latLng = function() {
 		if (self.lat === 0 || self.lon === 0) {
 			return null;
 		} else {
 			return new google.maps.LatLng(self.lat, self.lng);
 		}
 	};

 	self.marker = (function() {
 		if (self.lat !== 0 && self.lng !== 0) {
 			var marker = new google.maps.Marker({
				position: new google.maps.LatLng(self.lat, self.lng),
				map: map,
				icon: defaultIcon
			});
			markers.push(marker);
			return marker;
 		}
 	})(self);

	//this function for rendring my retrieved data from foursquare api as html code
 	self.formattedInfoWindowData = function() {
 		return '<div class="window-content">' +
 			'<span class="window-header"><h5>' + (self.name === undefined ? 'No name available' : self.name) + '</h5>' +
 			'<h6>' + (self.formattedAddress === undefined ? 'No address available' : self.formattedAddress) + '</h6><br>' +
 			(self.checkinsCount === undefined ? '' : '<h6>Number of checkins: ' + self.checkinsCount + '</h6>') +
 			'</div>';
 	};

};


// i used Project_Code_13_DevilInTheDetailsPlacesDetails starter code in git hub for
// the functions beow

 // This function populates the infowindow when the marker is clicked. We'll only allow
 // one infowindow which will open at the marker that is clicked, and populate based
 // on that markers position.

 function populateInfoWindow(marker, infowindow, content) {
 // Check to make sure the infowindow is not already opened on this marker.
 if (infowindow.marker != marker) {
 	// Clear the infowindow content to give the streetview time to load.
 	infowindow.setContent('');
 	infowindow.marker = marker;
 	// Make sure the marker property is cleared if the infowindow is closed.
 	infowindow.addListener('closeclick', function() {
 		if (infowindow.marker !== null)
 			infowindow.marker.setAnimation(null);
 		infowindow.marker = null;
 	});

	//unfortunately my Archaeological Mosques api dosen't have any streetview images from google
	//the function works fine but there is no images in my site
 	var streetViewService = new google.maps.StreetViewService();
 	var radius = 50;

 	// Use streetview service to get the closest streetview image within
 	// 50 meters of the markers position
 	streetViewService.getPanoramaByLocation(marker.position, radius, function(data, status) {
 		if (status == google.maps.StreetViewStatus.OK) {
 			var nearStreetViewLocation = data.location.latLng;
 			var heading = google.maps.geometry.spherical.computeHeading(
 				nearStreetViewLocation, marker.position);
 			infowindow.setContent('<div id="pano"></div>' + content);
 			var panoramaOptions = {
 				position: nearStreetViewLocation,
 				pov: {
 					heading: heading,
 					pitch: 30
 				}
 			};
 			var panorama = new google.maps.StreetViewPanorama(
 				document.getElementById('pano'), panoramaOptions);
 		} else {
 			infowindow.setContent('<div>No Street View Found</div>' + content);
 		}
 	});
 	// Open the infowindow on the correct marker.
 	infowindow.open(map, marker);
 }
 }
