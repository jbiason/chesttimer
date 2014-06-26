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

chesttimerModule.controller('CharacterController', function (Sexes, Characters, $scope) {
  $scope.sexes = Sexes.query();
  $scope.groups = Characters.query();
});
