'use strict';


var MenuGen = angular.module('MenuGen', [
    'ui.router',
    'ui.bootstrap'
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
                $injector.get("$state").go("login", {destination: $location.path()});
            }
            return response || $q.when(response);
        },
        'responseError': function (rejection, $state) {
            if (rejection.status == 401) {
                console.log("Rejection received while accessing " + rejection.config.url +
                    ", redirecting to login screen...");
                $window.sessionStorage.token = null;
                $window.sessionStorage.username = null;
                $injector.get('$state').transitionTo('login');
            }
            return $q.reject(rejection);
        }
    };
}]);

MenuGen.config([
    '$stateProvider', '$urlRouterProvider', '$urlMatcherFactoryProvider', '$httpProvider',
    function ($stateProvider, $urlRouterProvider, $urlMatcherFactory, $httpProvider) {
        $urlRouterProvider.otherwise("login");
        $urlMatcherFactory.caseInsensitive(true);
        $httpProvider.interceptors.push('authInterceptor');

        $stateProvider
            .state('home', {
                url: '/',
                templateUrl: 'templates/app.html',
                controller: 'HomeController',
                resolve: {}
            });
    }]);
