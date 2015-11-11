'use strict';


var MenuGen = angular.module('MenuGen', [
    'ui.router',
    'MenuGen.services'
]);

MenuGen.config(config);
MenuGen.run(run);

config.$inject = ['$stateProvider', '$urlRouterProvider', '$urlMatcherFactoryProvider', '$httpProvider'];
function config ($stateProvider, $urlRouterProvider, $urlMatcherFactory, $httpProvider) {
    $urlRouterProvider.otherwise("/");
    $urlMatcherFactory.caseInsensitive(true);

    $stateProvider
        .state('landing', {
            url: '^/',
            templateUrl: 'static/views/landing.html',
            controller: 'LandingController',
            resolve: {
                authenticated: ['AuthenticationService', function(AuthenticationService){
                    return AuthenticationService.authenticationStatus();
                }]
            }
        })
        .state('login', {
            url: '/login',
            templateUrl: 'static/views/login.html',
            controller: 'LoginController',
            resolve: {
                authenticated: ['AuthenticationService', function (AuthenticationService) {
                    return AuthenticationService.authenticationStatus();
                }]
            }
        })
        .state('register', {
            url: '/register',
            templateUrl: 'static/views/register.html',
            controller: 'RegisterController',
            resolve: {
                authenticated: ['AuthenticationService', function(AuthenticationService){
                    return AuthenticationService.authenticationStatus();
                }]
            }
        })
        .state('tastes', {
            url: '/tastes',
            templateUrl: 'static/views/tastes.html',
            controller: 'TastesController'
        });
}

run.$inject = ['AuthenticationService'];
function run(AuthenticationService){
    AuthenticationService.initialize('//127.0.0.1:8000/rest-auth', false);
}