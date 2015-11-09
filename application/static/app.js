'use strict';


var MenuGen = angular.module('MenuGen', [
    'ui.router',
    'MenuGen.services'
]);

MenuGen.factory('authInterceptor', ['$injector', '$location', '$rootScope', '$q', '$window', function ($injector, $location, $rootScope, $q, $window) {
    return {
        request: function (config) {
            config.headers = config.headers || {};
            console.log("Stored session token:", $window.sessionStorage.token);
            if ($window.sessionStorage.token && $window.sessionStorage.token !== "null") {
                config.headers.Authorization = 'Bearer ' + $window.sessionStorage.token;
            }
            return config;
        },
        response: function (response) {
            if (response.status == 401) {
                console.log("Got unauthorized while accessing " + response.config.url);
                $injector.get("$state").go("landing", {destination: $location.path()});
                console.log("Redirect after response 401.");
            }
            return response || $q.when(response);
        },
        'responseError': function (rejection, $state) {
            if (rejection.status == 401) {
                console.log("Rejection received while accessing " + rejection.config.url +
                    ", redirecting to login screen...");
                $window.sessionStorage.token = null;
                $window.sessionStorage.username = null;
                console.log("Redirect after rejection 401.");
                $injector.get('$state').transitionTo('landing');
            }
            return $q.reject(rejection);
        }
    };
}]);

MenuGen.config([
    '$stateProvider', '$urlRouterProvider', '$urlMatcherFactoryProvider', '$httpProvider',
    function ($stateProvider, $urlRouterProvider, $urlMatcherFactory, $httpProvider) {
        $urlRouterProvider.otherwise("/");
        $urlMatcherFactory.caseInsensitive(true);
        $httpProvider.interceptors.push('authInterceptor');

        $stateProvider
            .state('landing', {
                url: '^/',
                templateUrl: 'static/views/landing.html',
                controller: 'LandingController',
                resolve: {}
            })
            .state('tastes', {
                url: '/tastes',
                templateUrl: 'static/views/tastes.html',
                controller: 'TastesController'
            });
    }]);
