var $mainContainer = $('#main-container')
var $loader = $('#loader')
var $addArea = $('#add-area')

$(window).load(function() {
	$loader.hide()
	$mainContainer.show();
});

$addArea.click(function(){
	$('#modal1').modal('open');
});

angular.module('mainApp', ['ngResource'])

	.controller('MainCtrl', ['$scope', 'KnowledgeAreaService', function($s, KnowledgeAreaService){
		console.log('$s.user:', $s.user)


		$s.areas = [];

		KnowledgeAreaService.query(function(data) {
			$s.contents = data;
		});

		$s.initializeAreas = function(data) {
			$s.areas = data
		}
		$s.addArea = function() {
			obj = {
				pk: $s.areas.length,
				name: `area-${$s.areas.length}`
			}
			console.log('obj:', obj)
			$s.areas.push(obj)
		}

	}])

	.directive('clickToFirstTab', function() {
	  return function(scope, element, attrs) {
	  	angular.element(element).attr('href', `#area${scope.$index}`)
	      if (scope.$last){
	      	$('ul.tabs').tabs();
	      }
	  };
	})
	.directive('showFirstContentTab', function() {
	  return function(scope, element, attrs) {
	  	angular.element(element).attr('id', `area${scope.$index}`)
	  	if (scope.$last){
	  		angular.element(element).css('display', 'none')
	  		scope.initializeAreas(scope.contents)
	  	}
	  };
	})