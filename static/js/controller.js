/*
Cisco CDR Parser v1.0
(c) 2016 David Todd, https://github.com/alopexc0de/CDRParser
License: MIT
*/
var app = angular.module('MyApp', ['ngMaterial','tableSort',]).controller('logviewer', function($scope, $http, $mdDialog){
    var tmp = [];
    var list = '[[bigData]]'; // Pull in information provided by bottle's template engine
    data = list.replace(/&quot;/g, '"'); // For some reason the quotes become HTMLescaped when retrieved from bottle, replace those with normal quotes
    data = JSON.parse(data); // Our data is already JSON, but it acts as a string before this stage
    data.forEach(function(d){
        // Rearrange Cisco's weird date format to something Javascript can understand and convert it to UNIX time
        // First 17 characters are the time including timezone
        // Remaining characters are the date
        // This moves the first 17 characters to after a space 
        d.connect = Date.parse(d.connect.slice(17) + ' ' + d.connect.slice(0, 17)); 
        d.disconnect = Date.parse(d.disconnect.slice(17) + ' ' + d.disconnect.slice(0, 17));
        tmp.push(d);
    });

    $scope.origins = [
        'originate',
        'answer'
    ];

    $scope.getfiltered = function(){
        $scope.data = [];
        var tmpdata = [];
        var thedata = tmp; // Use date-corrected data from the above data.forEach
        thedata.forEach(function(d){
            if (!$scope.query.username &&
                !$scope.query.origin &&
                !$scope.query.from &&
                !$scope.query.to){ // no query

                tmpdata = tmp;
            }
            else if (d.username.indexOf($scope.query.username) != -1 && $scope.query.username != ''){
                // the user searched for a specific username
                tmpdata.push(d);
            }
            else if (d.origin.indexOf($scope.query.origin) != -1 && $scope.query.origin != ''){
                // the user searched for a specific origin (either originate or answer)
                tmpdata.push(d);
            }
            else if (d.calling.indexOf($scope.query.from) != -1 && $scope.query.from != ''){
                // the user searched for a specific caller
                tmpdata.push(d);
            }
            else if (d.called.indexOf($scope.query.to) != -1 && $scope.query.to != ''){
                // the user searched for a specific callee
                tmpdata.push(d);
            }
        });

        // Remove any duplicates
        tmpdata.forEach(function(d){
            if($scope.data.indexOf(d) === -1){
                $scope.data.push(d);
            }
        });
    };
    $scope.resetquery = function(){ // Sets the query to default blank state
        $scope.query = {
            username: '',
            origin: '',
            from: '',
            to: '',
        };
    };
    $scope.resetquery();

    $scope.$watch('query', $scope.getfiltered, true); // Automatically search after the debounce is over
});