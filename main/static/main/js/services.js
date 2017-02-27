angular.module('mainApp')

.factory('KnowledgeAreaService', ['$resource', function($resource) {
	return $resource('/services/knowledge-areas/', null, { 'update': { method:'PUT' } });
}])
.factory('ThemeService', ['$resource', function($resource) {
	return $resource('/services/knowledge-areas/:id/themes/', null, { 'update': { method:'PUT' } });
}])
.factory('IssueService', ['$resource', function($resource) {
	return $resource('/services/themes/:theme_id/issues/:id/', null, { 'update': { method:'PUT' } });
}])
