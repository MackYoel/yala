angular.module('mainApp')

.factory('KnowledgeAreaService', ['$resource', function($resource) {
	return $resource('/services/knowledge-areas/', null, { 'update': { method:'PUT' } });
}]);