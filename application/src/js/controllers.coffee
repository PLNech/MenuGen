tweeterControllers = angular.module('tweeterApp.controllers', [])
tweeterControllers.controller 'TweetCtrl', ($scope, Tweet) ->
  $scope.tweets = {}
  Tweet.query (response) ->
    $scope.tweets = response
    return

  $scope.submitTweet = (text) ->
    tweet = new Tweet(text: text)
    tweet.$save ->
      $scope.tweets.unshift tweet
      return
    return

  return
tweeterControllers.controller 'UserCtrl', ($scope, Tweet, User, AuthUser) ->
  $scope.tweets = {}
  id = AuthUser.id
  User.get { id: id }, (response) ->
    $scope.user = response
    $scope.tweets = response.tweets
    return
  return
