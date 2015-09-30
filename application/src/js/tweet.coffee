appendNewTweet = (tweet) ->
  newTweet = '<div class=\'tweet-container\'>' + '<div class=\'tweet-time\'>' + new Date(tweet.time).toLocaleString() + '</div>' + '<div class=\'tweet-body\'>' + tweet.text + '</div>' + '</div>'
  $('#tweets-target').prepend newTweet
  return

$.ajax
  type: 'GET'
  url: '/ajax'
  success: (data) ->
    i = 0
    while i < data.tweets.length
      appendNewTweet data.tweets[i]
      i++
    return
$('#tweet').click ->
  $.ajax
    type: 'POST'
    url: '/ajax'
    contentType: 'application/json'
    data: JSON.stringify(tweet: $('#new-tweet').val())
    success: (data) ->
      appendNewTweet data
      $('#new-tweet').val ''
      return
  return
