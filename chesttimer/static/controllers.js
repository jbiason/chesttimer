angular.module('ChestTimerApp', ['ngRoute'])
  .factory('Sexes', function () {
    return {male: 'Male',
            female: 'Female'};
  })

  .factory('Races', function () {
      return {norn: 'Norn',
              sylvari: 'Sylvari',
              human: 'Human',
              charr: 'Charr',
              asura: 'Asura'};
  })

  .factory('Orders', function () {
      return {order_of_whispers: 'Order of Whispers',
              vigil: 'Vigil',
              durmand_priori: 'Durmand Priori'};
  })

  .factory('Disciplines', function () {
      return {armorsmith: 'Armorsmith',
              weaponsmith: 'Weaponsmith',
              artificer: 'Artificer',
              chef: 'Chef',
              tailor: 'Tailor',
              huntsman: 'Huntsman',
              jeweler: 'Jeweler',
              leatherworker: 'Leatherworker'};
  })

  .factory('Professions', function() {
      return {guardian: 'Guardian',
              warrior: 'Warrior',
              necromancer: 'Necromancer',
              mesmer: 'Mesmer',
              elementalist: 'Elementalist',
              ranger: 'Ranger',
              thief: 'Thief',
              engineer: 'Engineer'};
  })

  .factory('Characters', function () {
    return [{characters: [{disciplines: null,
                           level: 25,
                           name: "Sgt Buzzkill",
                           order: null,
                           profession: "warrior",
                           race: "human",
                           sex: "female",
                           slug: "sgt_buzzkill"}],
             group: 25},
            {characters: [{disciplines: {armorsmith: 500,
                                         weaponsmith: 415},
                           level: 80,
                           name: "Thorianar",
                           order: "durmand_priori",
                           profession: "guardian",
                           race: "charr",
                           sex: "male",
                           slug: "thorianar"},
                          {disciplines: {huntsman: 400,
                                         leatherworker: 500},
                           level: 80,
                           name: "Commander Buzzkill",
                           order: "durmand_priori",
                           profession: "engineer",
                           race: "charr",
                           sex: "male",
                           slug: "commander_buzzkill"}],
             group: 80}];
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

  .controller('CharacterController', function ($scope, Sexes, Races, Orders,
                                               Disciplines, Professions, Characters) {
    $scope.sexes = Sexes;
    $scope.races = Races;
    $scope.orders = Orders;
    $scope.disciplines = Disciplines;
    $scope.professions = Professions;
    $scope.characters = Characters;
  })
;
