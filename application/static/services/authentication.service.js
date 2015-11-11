/**
 * Created by kiyoakimenager on 09/11/2015.
 */
'use strict';

angular
    .module('MenuGen.services')
    .service('AuthenticationService', AuthenticationService);


AuthenticationService.$inject = ['$q', '$http', '$cookies', '$rootScope'];
function AuthenticationService($q, $http, $cookies, $rootScope) {

    var service = {
        /* START CUSTOMIZATION HERE */
        // Change this to point to your Django REST Auth API
        // e.g. /api/rest-auth  (DO NOT INCLUDE ENDING SLASH)
        'API_URL': '//127.0.0.1:8000/rest-auth',
        // Set use_session to true to use Django sessions to store security token.
        // Set use_session to false to store the security token locally and transmit it as a custom header.
        'use_session': true,
        /* END OF CUSTOMIZATION */
        'authenticated': null,
        'authPromise': null
    };

    service.initialize = initialize;
    service.request = request;
    service.login = login;
    service.logout = logout;
    service.authenticationStatus = authenticationStatus;

    return service;

    function initialize (url, sessions) {
        this.API_URL = url;
        this.use_session = sessions;

        return this.authenticationStatus();
    }

    function request(args){
    // Let's retrieve the token from the cookie, if available
        if($cookies.get('token')){
            $http.defaults.headers.common.Authorization = 'Token ' + $cookies.get('token');
        }
        // Continue
        params = args.params || {}
        args = args || {};
        var deferred = $q.defer(),
            url = this.API_URL + args.url,
            method = args.method || "GET",
            params = params,
            data = args.data || {};
        // Fire the request, as configured.
        $http({
            url: url,
            withCredentials: this.use_session,
            method: method.toUpperCase(),
            headers: {'X-CSRFToken': $cookies.get('csrftoken')},
            params: params,
            data: data
        })
        .success(angular.bind(this,function(data, status, headers, config) {
            deferred.resolve(data, status);
        }))
        .error(angular.bind(this,function(data, status, headers, config) {
            console.log("error syncing with: " + url);
            // Set request status
            if(data){
                data.status = status;
            }
            if(status == 0){
                if(data == ""){
                    data = {};
                    data['status'] = 0;
                    data['non_field_errors'] = ["Could not connect. Please try again."];
                }
                // or if the data is null, then there was a timeout.
                if(data == null){
                    // Inject a non field error alerting the user
                    // that there's been a timeout error.
                    data = {};
                    data['status'] = 0;
                    data['non_field_errors'] = ["Server timed out. Please try again."];
                }
            }
            deferred.reject(data, status, headers, config);
        }));
        return deferred.promise;
    }

    function authenticationStatus (restrict, force){
        // Set restrict to true to reject the promise if not logged in
        // Set to false or omit to resolve when status is known
        // Set force to true to ignore stored value and query API
        restrict = restrict || false;
        force = force || false;
        if(this.authPromise == null || force){
            this.authPromise = this.request({
                'method': "GET",
                'url': "/user/"
            })
        }
        var da = this;
        var getAuthStatus = $q.defer();
        if(this.authenticated != null && !force){
            // We have a stored value which means we can pass it back right away.
            if(this.authenticated == false && restrict){
                getAuthStatus.reject("User is not logged in.");
            }else{
                getAuthStatus.resolve();
            }
        }else{
            // There isn't a stored value, or we're forcing a request back to
            // the API to get the authentication status.
            this.authPromise.then(function(){
                da.authenticated = true;
                getAuthStatus.resolve();
            },function(){
                da.authenticated = false;
                if(restrict){
                    getAuthStatus.reject("User is not logged in.");
                }else{
                    getAuthStatus.resolve();
                }
            });
        }
        return getAuthStatus.promise;
     }

    function login(username,password) {
        var authenticationService = this;

        return this.request({
            'method': "POST",
            'url': "/login/",
            'data':{
                'username':username,
                'password':password
            }
        }).then(function(data){
            if(!authenticationService.use_session){
                $http.defaults.headers.common.Authorization = 'Token ' + data.key;
                $cookies.put('token', data.key);
            }
            authenticationService.authenticated = true;
            $rootScope.$broadcast("djangoAuth.logged_in", data);
        });
    }

    function logout() {
        var authenticationService = this;

        return this.request({
            'method': "POST",
            'url': "/logout/"
        }).then(function(data){
            delete $http.defaults.headers.common.Authorization;
            $cookies.remove('token');
            delete $cookies.get('token');

            authenticationService.authenticated = false;
            $rootScope.$broadcast("djangoAuth.logged_out");
        });
    }
}
