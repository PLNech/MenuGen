// Resources have the following methods by default:
// get(), query(), save(), remove(), delete()

angular.module('MenuGen.services', ['ngResource'])
    .factory('Profile', function($resource) {
        return $resource('/api/profiles/:id/');
    });
