// Resources have the following methods by default:
// get(), query(), save(), remove(), delete()

angular.module('MenuGen.services', ['ngResource'])
    .factory('Profile', function($resource) {
        return $resource('/api/profiles/:id/');
    })
    .factory('SearchRecipe', function($resource) {
        return $resource('/api/recipes?name=:name');
    })
    .factory('SearchIngredient', function($resource) {
        return $resource('/api/ingredients?name=:name');
    });
