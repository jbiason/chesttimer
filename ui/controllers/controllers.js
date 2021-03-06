var serviceConfig = {query: {method: 'GET',
                             isArray: false,
                             cache: true}};

angular.module('ChestTimerApp', ['ngRoute', 'ngResource', 'mm.foundation', 'ChestTimerConfig'])
  .config(['$httpProvider', '$resourceProvider', function ($httpProvider, $resourceProvider) {
    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Request-With'];
    $resourceProvider.defaults.stripTrailingSlashes = false;
  }])

  .factory('Sexes', function ($resource, config) {
    return $resource(config.server + '/api/sexes/', {}, serviceConfig);
  })

  .factory('Races', function ($resource, config) {
    return $resource(config.server + '/api/races/', {}, serviceConfig);
  })

  .factory('Orders', function ($resource, config) {
    return $resource(config.server + '/api/orders/', {}, serviceConfig);
  })

  .factory('Disciplines', function ($resource, config) {
    return $resource(config.server + '/api/disciplines/', {}, serviceConfig);
  })

  .factory('Professions', function($resource, config) {
    return $resource(config.server + '/api/professions/', {}, serviceConfig);
  })

  .factory('Characters', function ($resource, config) {
    return $resource(config.server + '/api/characters/:slug',
      {slug: '@slug'},
      {query: {method: 'GET',
               isArray: false},
       update: {method: 'PUT'}}
      );
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

  .controller('CharacterController', function ($scope, $routeParams, $http, $modal,
        Sexes, Races, Orders, Disciplines, Professions,
        Characters) {
    $scope.sexes = {} ; $scope.races = {}; $scope.orders = {}; $scope.disciplines = {}; $scope.professions = {};
    $scope.listOrder = $routeParams.order;
    $scope.characters = [];

    // XXX None of those are checking the response.status, which is bad.
    Sexes.query(function (response) {
      $scope.sexes = response.sexes;
    }, function (error) {
      console.log(error);
    });

    Races.query(function (response) {
      $scope.races = response.races;
    }, function (error) {
      console.log(error);
    });

    Orders.query(function (response) {
      $scope.orders = response.orders;
    }, function (error) {
      console.log(error);
    });

    Disciplines.query(function (response) {
      $scope.disciplines = response.disciplines;
    }, function(error) {
      console.log(error);
    });

    Professions.query(function (response) {
      $scope.professions = response.professions;
    }, function(error) {
      console.log(error);
    });

    // methods
    $scope.edit = function (group, index) {
      $scope._edit_modal($scope.characters[group].characters[index]);
    };

    $scope.add = function () {
      $scope._edit_modal(null);
    };

    $scope.delete = function (group, index) {
      var character = $scope.characters[group].characters[index];
      var modal = $modal.open({
        templateUrl: 'delete-character-confirmation',
          controller: 'DeleteCharacterController',
          windowClass: 'small',
          resolve: {
            character: function () { return character; }
          }
      });

      modal.result.then(function () {
        $scope._load_characters();
      });
    };

    $scope._load_characters = function () {
      console.log('Reloading...');
      Characters.query({order: $scope.listOrder}, function (response) {
        $scope.characters = response.groups;
      }, function (error) {
        console.log(error);
      });
    };

    $scope._edit_modal = function(selected) {
      var modal = $modal.open({
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

      modal.result.then(function () {
        // due the way we deal with grouping and stuff, we need to ask the
        // server for new results.
        $scope._load_characters();
      });
    };

    // first load
    $scope._load_characters();
  })

  .controller('EditCharacterController', function ($scope, $modalInstance,
        sexes, races, orders, disciplines, professions, character, Characters) {
    $scope.sexes = sexes;
    $scope.races = races;
    $scope.orders = orders;
    $scope.disciplines = disciplines;
    $scope.professions = professions;

    if (character) {
      $scope.character = character;
      $scope.isNew = false;
    } else {
      $scope.character = {};
      $scope.isNew = true;
    }

    $scope.close = function () {
      $modalInstance.dismiss('cancel');
    };

    $scope.save = function () {
      if ($scope.isNew) {
        Characters.save($scope.character, function (response) {
          $modalInstance.close();
        }, function (error) {
          console.log(error);
        });
      } else {
        $scope.character.slug = $scope.character.name.toLowerCase().replace(' ', '_', 'g');
        console.log($scope.character.slug);

        Characters.update($scope.character, function(response) {
          // success
          $modalInstance.close();
        }, function (error) {
          /// error
          console.log(error);
        });
      }
    };
  })

  .controller('DeleteCharacterController', function ($scope, $modalInstance,
        character, Characters) {
    $scope.character = character; 
    
    $scope.close = function () {
      $modalInstance.dismiss();
    };

    $scope.delete = function () {
      var slug = $scope.character.name.toLowerCase().replace(' ', '_', 'g');

      Characters.get({slug: slug, method: 'DELETE'}, function (response) {
        console.log(response);
        $modalInstance.close();
      }, function (error) {
        console.log(error);
      });
    };
  })
;
