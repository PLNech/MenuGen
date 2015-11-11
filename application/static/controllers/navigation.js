/**
 * Created by kiyoakimenager on 10/11/2015.
 */

'use strict';

angular.module('MenuGen.services')
    .controller('NavigationController', function ($scope, $uibModal, $location, AuthenticationService, $log) {
        // Assume user is not logged in until we hear otherwise
        $scope.authenticated = false;
          // Wait for the status of authentication, set scope var to true if it resolves
          AuthenticationService.authenticationStatus(true).then(function(){
              $scope.authenticated = true;
          });
          // Wait and respond to the logout event.
          $scope.$on('djangoAuth.logged_out', function() {
            $scope.authenticated = false;
          });
          // Wait and respond to the log in event.
          $scope.$on('djangoAuth.logged_in', function() {
            $scope.authenticated = true;
          });
          // If the user attempts to access a restricted page, redirect them back to the main page.
          $scope.$on('$routeChangeError', function(ev, current, previous, rejection){
            console.error("Unable to change routes.  Error: ", rejection)
            $location.path('/restricted').replace();
          });

          $scope.logout = function(){
            AuthenticationService.logout();
            //.then(handleSuccess,handleError);
          }

          // Modal
          $scope.animationsEnabled = true;

          $scope.openModal = function (size, template, controller) {
              $scope.$modalInstance = $uibModal.open({
                      scope: $scope,
                      animation: $scope.animationsEnabled,
                      templateUrl: template,
                      controller: controller,
                      size: size,
                      resolve: {}
                  }
              );

              $scope.$modalInstance.result.then(function (selectedItem) {
                  $scope.selected = selectedItem;
              }, function () {
          $log.info('Modal dismissed');
        });
      };

      $scope.toggleAnimation = function () {
        $scope.animationsEnabled = !$scope.animationsEnabled;
      };

    });


