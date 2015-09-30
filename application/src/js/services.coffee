# Resources have the following methods by default:
# get(), query(), save(), remove(), delete()
angular.module('tweeterApp.services', [ 'ngResource' ]).factory('Tweet', ($resource) ->
  $resource '/api/tweets/:id/'
).factory 'User', ($resource) ->
  $resource '/api/users/:id/'
