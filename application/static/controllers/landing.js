'use strict';

angular.module('MenuGen').
    controller('LandingController', ['$scope', function ($scope, AuthenticationService) {
        $scope.username = "asd";
        console.log("End of controller execution.");

        $scope.update = function () {
            $scope.username =
                $scope.username == "asd" ?
                    "dsa" : "asd";
            console.log($scope.username);
        };
    }]);
