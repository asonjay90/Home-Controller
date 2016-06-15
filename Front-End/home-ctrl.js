var app = angular.module('HomeCtrl',['ngMaterial', "ngRoute"])

app.config(function($mdIconProvider, $routeProvider, $locationProvider) {
    $mdIconProvider
       .iconSet('social', 'img/icons/sets/social-icons.svg', 24)
       .defaultIconSet('img/icons/sets/core-icons.svg', 24);   
    $routeProvider.
      when('/lights', {templateUrl: 'remotes/lights.html',   controller: lightCtrl }).
      when('/av', {templateUrl: 'remotes/av.html',   controller: avCtrl }).
      when('/hvac', {templateUrl: 'remotes/hvac.html',   controller: hvacCtrl }).
      otherwise({redirectTo: '/lights'});
   });

app.controller('tempCtrl', function($scope, $interval, $http) {
    $scope.currentTemp = "Getting Temperature...";
    $scope.currentTempMetric = 'f'
    $interval(function() {
        $scope.getTemp();
        }, 60000);

    $scope.getTemp = function() {
        $http({
            method : "GET",
            url : "http://room-controller/temp"
        }).then(function Succes(response) {
            $scope.currentTemp = $scope.formatTemp(response.data);
        }, function Error(response) {
            return response.statusText;
        });
    };    
    $scope.formatTemp = function(temp) {
        if ($scope.currentTempMetric == 'c') {
            return temp + " C";
        };
        if ($scope.currentTempMetric == 'f') {
            tempF = parseFloat(temp) * 1.8 + 32;
            return tempF.toFixed(2) + " F";
        };
    };    
    $scope.changeMetric = function() {
        if ($scope.currentTempMetric == 'c') {
            $scope.currentTempMetric = 'f';
            $scope.getTemp();
        }
        else {
            $scope.currentTempMetric = 'c';
            $scope.getTemp();            
        }
    };
});

app.controller('tabCtrl', function($scope, $location) {
    $scope.lights = {}
    $scope.av = {}
    $scope.hvac = {}
    $scope.selectedIndex = 0;

    $scope.$watch('selectedIndex', function(current, old) {
        switch (current) {
            case 0:
                $location.url("/lights");
                break;
            case 1:
                $location.url("/av");
                break;
            case 2:
                $location.url("/hvac");
                break;
        }
    });
});

app.controller('requestCtrl', function($scope, $http, $mdToast) {
    
    $scope.sendRequest = function(device, action, method='POST') {
        $http({
        method : method,
        url : "http://room-controller/" + device + "/" + action
    }).then(function Succes(response) {
       $mdToast.show($mdToast.simple().textContent(response.data));
    }, function Error(response) {
        var errMsg = "Error - Can't Reach Controller!";
        $mdToast.show($mdToast.simple().textContent(errMsg));
    });  
  };
  
  $scope.NexusControl = function($event) {
    var key = $event.keyCode;
    switch (key) {
      case 38:
        $scope.sendRequest('nexus', 'nav_up');
        break;
      case 40:
        $scope.sendRequest('nexus', 'nav_down');
        break;
      case 37:
        $scope.sendRequest('nexus', 'nav_left');
        break;
      case 39:
        $scope.sendRequest('nexus', 'nav_right');
        break;
      case 13:
        $scope.sendRequest('nexus', 'nav_select');
        break;
      case 188:
        $scope.sendRequest('nexus', 'nav_back');
        break;
      case 190:
        $scope.sendRequest('nexus', 'nav_home');
        break;
    }
  };
});
    

function lightCtrl($scope) {
    $scope.lights.ceiling = [
        { name: 'All Off', button:'alloff', enabled: false },
        { name: 'Row 1', button:'row1', enabled: false },
        { name: 'Row 2', button:'row2', enabled: false },
        { name: 'Row 3', button:'row3', enabled: false },
    ];
    $scope.lights.hue = [
        { name: 'Power Off', button:'power_off', enabled:false},
        { name: 'Energize', button:'preset1', enabled:false},
        { name: 'Sunset', button:'preset2', enabled:false},
	    { name: 'Love Shack', button:'preset3', enabled:false},
    ];
};

function avCtrl($scope) {
    $scope.av.tv = [
        { name: 'Watch TV', button:'watchtv', enabled:false},
	    { name: 'Power Off', button:'alloff', enabled:false},
	];	
	$scope.av.receiver = [
        { name: 'Receiver Power', button:'power', enabled:false},
	    { name: 'Volume Up', button:'vol_up', enabled:false},
	    { name: 'Volume Down', button:'vol_down', enabled:false},
	    { name: 'Input: Nexus', button:'input1', enabled:false},
	    { name: 'Input: PC', button: 'input2', enabled:false},
    ];
};

function hvacCtrl($scope) {
    $scope.hvac.fan = [
        { name: 'Power', button:'power', enabled:false},
	    { name: 'Speed', button:'speed', enabled:false},
	    { name: 'Oscillate', button:'oscillate', enabled:false},
    ];  
    $scope.hvac.ac = [
        { name: 'Power On', button:'pwron', enabled:false},
        { name: 'Power Off', button:'pwroff', enabled:false},
    ];
  
};
