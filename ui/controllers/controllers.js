angular.module('ChestTimerApp', ['ngRoute', 'mm.foundation'])
  .config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Request-With'];
  }])

  .factory('Sexes', function ($http) {
    var api = {};
    api.query = function () {
      return $http.get('http://127.0.0.1:5000/api/sexes/');
    };
    return api;
  })

  .factory('Races', function ($http) {
    var api = {};
    api.query = function () {
      return $http.get('http://127.0.0.1:5000/api/races/');
    };
    return api;
  })

  .factory('Orders', function ($http) {
    var api = {};
    api.query = function () {
      return $http.get('http://127.0.0.1:5000/api/orders/');
    };
    return api;
  })

  .factory('Disciplines', function ($http) {
    var api = {};
    api.query = function () {
      return $http.get('http://127.0.0.1:5000/api/disciplines/');
    };
    return api;
  })

  .factory('Professions', function($http) {
    var api = {};
    api.query = function () {
      return $http.get('http://127.0.0.1:5000/api/professions/');
    };
    return api;
  })

  .factory('Characters', function ($http) {
    var characters = {};
    characters.query = function (order) {
      order = order || 'level';
      return $http.get('http://127.0.0.1:5000/api/characters/?order=' + order);
    };
    return characters;
  })

  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        controller: 'MainCtrl',
        templateUrl: 'main.html'
      })
      .when('/characters', {
        redirectTo: '/character/level'
      })
      .when('/characters/:order', {
        controller: 'CharacterController',
        templateUrl: 'characters.html'
      });
  })

  .controller('MainCtrl', function ($scope) {
    // empty, for now
  })

  .controller('CharacterController', function ($scope, $routeParams, $http, $modal, Sexes, 
                                               Races, Orders, Disciplines, Professions,
                                               Characters) {
    $scope.sexes = {} ; $scope.races = {}; $scope.orders = {}; $scope.disciplines = {}; $scope.professions = {};
    $scope.listOrder = $routeParams.order;
    $scope.characters = [];

    // XXX None of those are checking the response.status, which is bad.
    Sexes.query().success(function (response) {
      $scope.sexes = response.sexes;
    });

    Races.query().success(function (response) {
      $scope.races = response.races;
    });

    Orders.query().success(function (response) {
      $scope.orders = response.orders;
    });

    Disciplines.query().success(function (response) {
      $scope.disciplines = response.disciplines;
    });

    Professions.query().success(function (response) {
      $scope.professions = response.professions;
    });

    Characters.query($scope.listOrder).success(function (response) {
      $scope.characters = response.groups;
    });

    // methods
    $scope.edit = function (group, index) {
      console.log(group, index);
      var selected = $scope.characters[group].characters[index];
      console.log(selected);
      $modal.open({
        templateUrl: 'edit-character-content',
        controller: 'EditCharacterController',
        resolve: {
          sexes: function () { return $scope.sexes; },
          races: function () { return $scope.races; },
          orders: function () { return $scope.orders; },
          disciplines: function () { return $scope.disciplines; },
          professions: function () { return $scope.professions; },
          character: function () { return selected; }
        }
      });
    };
  })

  .controller('EditCharacterController', function ($scope, $modalInstance, sexes, races, orders, disciplines, professions, character) {
    $scope.sexes = sexes;
    $scope.races = races;
    $scope.orders = orders;
    $scope.disciplines = disciplines;
    $scope.professions = professions;

    if (character) {
      $scope.character = character;
    } else {
      $scope.character = {};
    }

    $scope.close = function () {
      $modalInstance.dismiss('cancel');
    };
  })
;
