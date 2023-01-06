let app = angular.module("MyApp", [])

app.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
}]);

app.controller("signupCtrl", ['$scope', '$http', function($scope, $http) {
    $scope.errorText = ""
    $scope.username = ""
    $scope.email = ""
    $scope.password = ""
    $scope.confirm = ""
    $scope.handleClick = () => {
        $scope.errorText = ""
        if($scope.username.length == 0) {
            $scope.errorText = "Username is required"
            return
        }
        if($scope.email.length == 0) {
            $scope.errorText = "email is required"
            return
        }
        if($scope.password.length == 0) {
            $scope.errorText = "Password is required"
            return
        }
        if($scope.confirm != $scope.password) {
            $scope.errorText = "The passwords you entered do not match"
            return
        }
        let data = {
            "username": $scope.username,
            "email": $scope.email,
            "password": $scope.password
        }
        $http.post('/user/create', data)
            .then(res => {
                console.log(res.data.status)
                if(res.data.status == "200") {
                    sessionStorage.setItem("currentUser", JSON.stringify({
                        username: res.data.username,
                        files: []
                    }))
                    window.location = '/dashboard'
                } else {
                    $scope.errorText = res.data.message
                }
            })
    }
}])

app.controller("loginCtrl", ['$scope', '$http', function($scope, $http) {
    $scope.errorText = ""
    $scope.username = ""
    $scope.password = ""
    $scope.handleClick = () => {
        $scope.errorText = ""
        if($scope.username.length == 0) {
            $scope.errorText = "Username is required"
            return
        }
        if($scope.password.length == 0) {
            $scope.errorText = "Password is required"
            return
        }
        let data = {
            "username": $scope.username,
            "password": $scope.password
        }
        $http.post('/user/login', data)
            .then(res => {
                console.log(res.data.status)
                if(res.data.status == "200") {
                    sessionStorage.setItem("currentUser", JSON.stringify({
                        username: res.data.username,
                        files: res.data.files
                    }))
                    window.location = '/dashboard'
                } else {
                    $scope.errorText = res.data.message
                }
            })
    }
}])

app.controller("dashboardCtrl", ['$scope', function($scope) {
    $scope.user = JSON.parse(sessionStorage.getItem('currentUser'))
}])