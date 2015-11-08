'use strict';

angular.module('MenuGen').
    controller('TastesController', ['$scope', '$resource', 'Profile', 'SearchRecipe', 'SearchIngredient',
        function ($scope, $resource, Profile, SearchRecipe, SearchIngredient) {

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
                    });
                });

                // fetch the recipes not liked
                var recipes = $scope.profile.unlikes_recipe;
                $scope.not_liked_recipes = [];
                angular.forEach(recipes, function(recipe) {
                    var res = $resource(recipe);
                    res.get(function(resource) {
                        $scope.not_liked_recipes.push(resource);
                    });
                });
            });

            // search for ingredients and recipes
            $scope.search = function() {
                SearchRecipe.query({name:$scope.input}, function(response) {
                    $scope.found_recipes = response;
                });
                SearchIngredient.query({name:$scope.input}, function(response) {
                    $scope.found_ingredients = response;
                });
            };

            // relike recipe
            $scope.relike = function(recipe) {
                var index = $scope.not_liked_recipes.indexOf(recipe);
                $scope.not_liked_recipes.splice(index, 1);
                // todo: update database
            };

            // relike ingredient
            $scope.relike_ingred = function(ingred) {
                var index = $scope.not_liked_ingreds.indexOf(ingred);
                $scope.not_liked_ingreds.splice(index, 1);
                // todo: update database
            }
        }
    ]);

