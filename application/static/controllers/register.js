/**
 * Created by kiyoakimenager on 09/11/2015.
 */

'use strict';

angular.module('MenuGen.services')
  .controller('RegisterController', function ($scope, $location, AuthenticationService, Validate) {
  	$scope.model = {'username':'','password':''};
  	$scope.complete = false;

        $scope.register = function(formData){
            $scope.errors = [];
            Validate.form_validation(formData,$scope.errors);
            if(!formData.$invalid){
                AuthenticationService.register($scope.model.username,$scope.model.password1,$scope.model.password2)
                    .then(function(data){
                        // success case
                        $location.path("/");
        	            $scope.complete = true;
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
