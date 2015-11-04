'use strict';

angular.module('MenuGen').
    controller('TastesController', ['$scope', '$resource', 'Profile', function ($scope, $resource, Profile) {
        // TODO: get profile of current user
        Profile.get({id:1}, function(response) {
            $scope.profile = response;

            // fetch the ingredients not liked
            var ingreds = $scope.profile.unlikes;
            $scope.not_liked_ingreds = [];
            angular.forEach(ingreds, function(ingred) {
                var res = $resource(ingred);
                res.get(function(resource) {
                    $scope.not_liked_ingreds.push(resource);
                })
            });

            // fetch the recipes not liked
            var recipes = $scope.profile.unlikes_recipe;
            $scope.not_liked_recipes = [];
            angular.forEach(recipes, function(recipe) {
                var res = $resource(recipe);
                res.get(function(resource) {
                    $scope.not_liked_recipes.push(resource);
                })
            });
        });
    }]);

