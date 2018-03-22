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
                            $scope.$broadcast('schemaForm.error.barcode','barcodeAlreadyTaken');
                        }
                    },
                    function errorCallback(response) {
                        $scope.$broadcast('schemaForm.error.barcode', 'barcodeCannotBeVerified');
                    }
                );
            } else {
              $scope.$broadcast('schemaForm.error.barcode','barcodeAlreadyTaken', true);
            }
        };
    }
);
