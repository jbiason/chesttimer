var chesttimerModule = angular.module('ChestTimer', []);

chesttimerModule.factory('Characters', function () {
  var chars = {};
  chars.query = function() {
    // ajax goes here
    return [{"characters": [{
      "disciplines": null,
      "level": 25,
      "name": "Sgt Buzzkill",
      "order": null,
      "profession": "warrior",
      "race": "human",
      "sex": "female",
      "slug": "sgt_buzzkill"
    }
    ],
    "group": 25
  },
  {
    "characters": [
    {
      "disciplines": {
        "armorsmith": 500,
        "weaponsmith": 415
      },
      "level": 80,
      "name": "Thorianar",
      "order": "durmand_priori",
      "profession": "guardian",
      "race": "charr",
      "sex": "male",
      "slug": "thorianar"
    },
    {
      "disciplines": {
        "huntsman": 400,
        "leatherworker": 500
      },
      "level": 80,
      "name": "Commander Buzzkill",
      "order": "durmand_priori",
      "profession": "engineer",
      "race": "charr",
      "sex": "male",
      "slug": "commander_buzzkill"
    }
    ],
    "group": 80
  }
  ];
};
  return chars;
});

chesttimerModule.factory('Sexes', function () {
  var sexes = {};
  sexes.query = function () {
    // ajax goes here
    return {male: 'Male',
            female: 'Female'};
  };
  return sexes;
});

chesttimerModule.factory('Races', function () {
  var races = {};
  races.query = function () {
    return {'norn': 'Norn',
    'sylvari': 'Sylvari',
    'human': 'Human',
    'charr': 'Charr',
    'asura': 'Asura'};
  };
  return races;
});

chesttimerModule.factory('Orders', function () {
  var orders = {};
  orders.query = function () {
    return {'order_of_whispers': 'Order of Whispers',
      'vigil': 'Vigil',
      'durmand_priori': 'Durmand Priori'};
  };
  return orders;
});

chesttimerModule.factory('Disciplines', function () {
  var disciplines = {};
  disciplines.query = function () {
    return {'armorsmith': 'Armorsmith',
      'weaponsmith': 'Weaponsmith',
      'artificer': 'Artificer',
      'chef': 'Chef',
      'tailor': 'Tailor',
      'huntsman': 'Huntsman',
      'jeweler': 'Jeweler',
      'leatherworker': 'Leatherworker'
    };
  };
  return disciplines;
});

chesttimerModule.factory('Professions', function () {
  var professions = {};
  professions.query = function () {
    return {'guardian': 'Guardian',
    'warrior': 'Warrior',
    'necromancer': 'Necromancer',
    'mesmer': 'Mesmer',
    'elementalist': 'Elementalist',
    'ranger': 'Ranger',
    'thief': 'Thief',
    'engineer': 'Engineer'};
  };
  return professions;
});

function routes($routeProvider) {
  $routeProvider.
    when('/characters/:order', {
      controller: CharacterController,
      templateUrl: 'characters.html'});
}
chesttimerModule.config(routes);

chesttimerModule.controller('CharacterController', function ($scope, Sexes, Races, Orders, Disciplines, Professions, Characters) {
  $scope.sexes = Sexes.query();
  $scope.races = Races.query();
  $scope.orders = Orders.query();
  $scope.disciplines = Disciplines.query();
  $scope.professions = Professions.query();
  $scope.groups = Characters.query();
});
