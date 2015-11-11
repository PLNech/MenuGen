/**
 * Created by kiyoakimenager on 09/11/2015.
 */

'use strict';

angular.module('MenuGen.services')
    .controller('LoginController', function ($scope, $location, AuthenticationService, Validate) {
        $scope.model = {'username':'','password':''};
  	    $scope.complete = false;

        $scope.login = function(formData){
            $scope.errors = [];
            Validate.form_validation(formData,$scope.errors);
            if(!formData.$invalid){
            AuthenticationService.login($scope.model.username, $scope.model.password)
                .then(function(data){
        	    // success case
        	        $location.path("/");
                    $scope.$modalInstance.dismiss('cancel');
            },function(data){
        	    // error case
        	    $scope.errors = data;
                });
            }
        }

        $scope.cancel = function () {
            $scope.$modalInstance.dismiss('cancel');
        };

  });
