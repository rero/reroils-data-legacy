angular.module('itemEditor', ['reroilsEditor'])
    .controller('ItemValidator', function($scope, $http, $window) {

        $scope.item = $scope.params.model;

        $scope.$watch('item.barcode', validateBarcode);

        function validateBarcode(newValue, oldValue, scope){
            if(newValue){
                var barcode = newValue;
                $http({
                    method: 'GET',
                    url: '/api/documents/?q=itemslist.barcode:' + barcode
                })
                .then(
                    function successCallback(response) {
                        if(response.data.hits.total > 0) {
                            if(scope.item.pid != response.data.hits.hits[0].metadata.itemslist[0].pid) {
                                $scope.$broadcast('schemaForm.error.barcode','alreadyTakenMessage');
                            }
                        }
                    },
                    function errorCallback(response) {
                        $scope.$broadcast('schemaForm.error.barcode', 'cannotBeVerifiedMessage');
                    }
                );
            } else {
                $scope.$broadcast('schemaForm.error.barcode','alreadyTakenMessage', true);
            }
        };
    }
);
