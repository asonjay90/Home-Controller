var app = angular.module('RoomController',['ngMaterial'])

.config(function($mdIconProvider) {
    $mdIconProvider
       .iconSet('social', 'img/icons/sets/social-icons.svg', 24)
       .defaultIconSet('img/icons/sets/core-icons.svg', 24);
   });

app.controller('ListCtrl', function($scope, $mdToast) {

  $scope.remote = {};
  $scope.nexus = 0;

  $scope.remote.ceiling = [
    { name: 'All Off', button:'alloff', enabled: false },
    { name: 'Row 1', button:'row1', enabled: false },
    { name: 'Row 2', button:'row2', enabled: false },
    { name: 'Row 3', button:'row3', enabled: false }
  ];

  $scope.remote.hue = [
    { name: 'Power Off', button:'power_off', enabled:false},
    { name: 'Energize', button:'preset1', enabled:false},
    { name: 'Sunset', button:'preset2', enabled:false},
	{ name: 'Love Shack', button:'preset3', enabled:false}
  ];
  
  $scope.remote.tv = [
    { name: 'Watch TV', button:'watchtv', enabled:false},
	{ name: 'Power Off', button:'alloff', enabled:false}
  ];
  
  $scope.remote.av = [
    { name: 'Receiver Power', button:'power', enabled:false},
	{ name: 'Volume Up', button:'vol_up', enabled:false},
	{ name: 'Volume Down', button:'vol_down', enabled:false},
	{ name: 'Input: Nexus', button:'input1', enabled:false},
	{ name: 'Input: PC', button: 'input2', enabled:false},
  ];
  
  $scope.remote.fan = [
    { name: 'Power', button:'power', enabled:false},
	{ name: 'Speed', button:'speed', enabled:false},
	{ name: 'Oscillate', button:'oscillate', enabled:false},
  ];
  
  $scope.remote.modes = [
    { name: 'Party On!', button:'on', enabled:false},
    { name: 'Party Off!', button:'off', enabled:false}
  ];
  
  $scope.NexusControl = function($event) {
    var key = $event.keyCode;
    //console.log(key);
    if (key == 38) {
      $scope.button('nav_up','nexus');
    }
    else if (key == 40) {
      $scope.button('nav_down','nexus');
    }
    else if (key ==37) {
      $scope.button('nav_left','nexus');
    }
    else if (key == 39) {
      $scope.button('nav_right','nexus');
    }
    else if ( key == 13) {
      $scope.button('nav_select','nexus');
    }
    else if ( key == 188) {
      $scope.button('nav_back','nexus');
    }
    else if ( key == 190) {
      $scope.button('nav_home','nexus');
    }
    
    
  }
  
  $scope.button = function(action,device) {
    var xmlHttp = new XMLHttpRequest();
    var theUrl = "http://room-controller/" + device + "/" + action;
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4){
            if (xmlHttp.status == 200){
                $mdToast.show($mdToast.simple().textContent(xmlHttp.responseText));
            }
            else {
                var errMsg = "Error - Can't Reach Controller!";
                $mdToast.show($mdToast.simple().textContent(errMsg));
            }
        };
    }
    xmlHttp.open( "POST", theUrl, true );
    xmlHttp.send(null);
  };

});
