"use strict";
var $mainContainer = $('#main-container')
var $loader = $('#loader')
var $addArea = $('#add-area')

$(window).load(function() {
	$loader.hide()
	$mainContainer.show();
});

angular.module('mainApp', ['ngResource'])
	.config(function($resourceProvider, $httpProvider) {
	  $resourceProvider.defaults.stripTrailingSlashes = false;
	  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
	  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	})

	.controller('MainCtrl', ['$scope', 'KnowledgeAreaService', 'ThemeService', 'IssueService', function($s, KnowledgeAreaService, ThemeService, IssueService){
		$s.loading = false
		$s.area = {}

		$s.wrap = function(label) {
			return $s.loading?'guardando':label
		};

		$s.message = function(modalId, ok, msg, time){
			msg = msg || ''
			msg = ok?`Ok! ${msg}`:`Oops! ${msg}`
			Materialize.toast(msg, time||2000)
			if (ok)
				$(modalId).modal('close')
			$s.loading = false
		}

		var modals = {
			area: {target: '.new-area-modal-target', id: '#new-area-modal'},
			theme: {target: '.new-theme-modal-target', id: '#new-theme-modal'},
			issue: {target: '.new-issue-modal-target', id: '#new-issue-modal'}
		};

		$s.areas = [];

		KnowledgeAreaService.query(function(areas) {
			if (!areas.length)
				return;
			$s.contents = areas;
			ThemeService.query({id: areas[0].pk}, function(themes) {
				$s.contents[0].themes = themes
				if ($s.areas.length){	
					$s.currentArea = $s.areas[0]
					if (themes.length)
						$s.currentArea.currentTheme = themes[0].pk
				}

			}, function(err) {
				console.log('err:', err)
			})

		});

		$s.initializeAreas = function(data) {
			$s.areas = data
		};

		$s.saveArea = function(data) {
			$s.loading = true
			KnowledgeAreaService.save(data, function(area){
				$s.message(modals.area.id, 1)
				$s.areas.push(area)
				if ($s.areas.length === 1) {
					$s.currentArea = area
					$s.contents = $s.areas;
				}

			}, function(err){
				var msg = err.data.name?err.data.name: null
				$s.message(modals.area.id, 0, msg)
			});
		}

		$s.saveTheme = function(theme, useCurrentArea) {
			if (useCurrentArea)
				theme.knowledge_area = $s.currentArea.pk;

			$s.loading = true
			ThemeService.save({id: theme.knowledge_area}, theme, function(theme){
				if (!Array.isArray($s.currentArea.themes)){
					$s.currentArea.themes = []
					$s.currentArea.currentTheme = theme.pk
				}
				$s.currentArea.themes.push(theme)
				$s.message(modals.theme.id, 1)
			}, function(err){
				$s.message(modals.theme.id, 0)
			});	
		};

		$s.getThemes = function(area) {
			$s.currentArea = area;
			if (area.themes && area.themes.length)
				return;

			console.log('querying')
			ThemeService.query({id: area.pk}, function(data) {
				updateThemes($s.contents, data)
			}, function(err) {
				console.log('err:', err)
			})
		};

		$s.setCurrentTheme = function(pk){
			$s.currentArea.currentTheme = pk
		}

		$s.saveIssue = function(issue, useCurrentTheme) {
			$s.loading = true
			if (useCurrentTheme)
				issue.theme = $s.currentArea.currentTheme;

			IssueService.save({theme_id: issue.theme}, issue, function(issue){
				var themeIndx = getObjectIndexByPk($s.currentArea.themes, issue.theme)
				$s.currentArea.themes[themeIndx].issues.push(issue)
				$s.message(modals.issue.id, 1)
			}, function(err){
				$s.message(modals.issue.id, 0)
				console.log('err:', err)
			})
		};

		$s.issueAction = function(issue, action){
			var params = {theme_id: issue.theme, id: issue.pk}
			if (action == 'complete')
				action = issue.completed?'complete':'open'

			params[action] = ''
			IssueService.update(params, {}, function(_issue){
				Object.assign(issue, _issue)
				Materialize.toast('actualizado', 1000)
			}, function(err) {
				Materialize.toast('Oops :(', 1000)
			})
		}

		$s.assignEvents = function(modal) {
			$(modals[modal].target).click(()=> {
				if (modal === 'theme' && !$s.currentArea)
					return;
				if (modal === 'issue' && (!$s.currentArea || !$s.currentArea.currentTheme))
					return;

				$(modals[modal].id).modal('open');
				$s.$apply(function(){
					$s[modal] = {};
				});
				$('select').val("")
				$('select').material_select()
			})
		}

		function updateThemes(objectList, themes) {
			// if (!themes.length)
			// 	return;

			var areaPk = themes[0].knowledge_area
			var area;

			for (var x = 0; x < objectList.length; x++) {
				area = objectList[x];
				if (area.pk === areaPk) {
					objectList[x].themes = themes
					objectList[x].currentTheme = themes[0].pk
					break;
				}
			}
		}

		function getObjectIndexByPk(list, pk) {
			var ind, obj;
			for (ind=0; ind< list.length; ind++) {
				obj = list[ind]
				if (obj.pk == pk)
					return ind
			}
			return -1
		}

	}])

	.directive('clickToFirstTab', function() {
	  return function(scope, element, attrs) {
	  	angular.element(element).attr('href', `#area${scope.$index}`)
	      if (scope.$last){
	      	// $('ul.tabs').tabs({swipeable: true});
	      	$('ul.tabs').tabs();
	      }
	  };
	})
	.directive('showFirstContentTab', function() {
	  return function(scope, element, attrs) {
	  	angular.element(element).attr('id', `area${scope.$index}`)
	  	if (scope.$last){
	  		// angular.element(element).css('display', 'none')
	  		scope.initializeAreas(scope.contents)
	  	}
	  };
	})
	.directive('initSelect', function() {
	  return function(scope, element, attrs) {
	  	  var obj = angular.element(element).attr('obj')
	  	  angular.element(element).html(scope[obj].name)
	      if (scope.$last){
	      	$('select').material_select();
	      }
	  };
	})
	.directive('initCollapsibles', function() {
	  return function(scope, element, attrs) {
	      if (scope.$last){
	      	$('.collapsible').collapsible();
	      }
	  };
	})
	.directive('showFirstTheme', function() {
	  return function(scope, element, attrs) {
	  	// angular.element(element).attr('id', `area${scope.$index}`)
	  	if (scope.$first){
	  		angular.element(element).addClass('active')
	  		// scope.initializeAreas(scope.contents)
	  	}
	  };
	})
