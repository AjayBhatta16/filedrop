let app = angular.module("MyApp", [])

app.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[')
    $interpolateProvider.endSymbol(']]')
}])

app.controller("homeCtrl", ['$scope', '$http', function($scope, $http) {
    $scope.currentUser = sessionStorage.getItem('currentUser')
    $scope.logout = () => {
        console.log('logout')
        sessionStorage.removeItem('currentUser')
        window.location = '/'
    }
    $scope.errorText = ""
    $scope.filecode = ""
    $scope.handleChange = () => {
        $scope.filecode = $scope.filecode.toUpperCase()
    }
    $scope.handleClick = () => {
        $scope.errorText = ""
        if($scope.filecode.length != 8) {
            $scope.errorText = "Please enter an 8-Digit File code"
            return
        }
        if(!/^[A-Za-z0-9]*$/.test($scope.filecode)) {
            $scope.errorText = "Please enter letters and numbers only"
            return 
        }
        $http({
            method: 'GET',
            url: `/${$scope.filecode}`,
        }).then(res => {
            let link = document.createElement('a')
            link.href = `/${$scope.filecode}`
            link.download = $scope.filecode
            document.body.appendChild(link)
            link.click()
            document.body.removeChild(link)
        }).catch(err => {
            $scope.errorText = "File code not found"
        })
    }
}])

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
    $scope.logout = () => {
        console.log('logout')
        sessionStorage.removeItem('currentUser')
        window.location = '/'
    }
    $scope.user = JSON.parse(sessionStorage.getItem('currentUser'))
}])

app.controller("newfileCtrl", ['$scope', '$http', function($scope, $http) {
    $scope.logout = () => {
        console.log('logout')
        sessionStorage.removeItem('currentUser')
        window.location = '/'
    }
    $scope.user = JSON.parse(sessionStorage.getItem('currentUser'))
    $scope.expDate = null
    $scope.errorText = ""
    $scope.handleUpload = () => {
        $scope.errorText = ""
        let file = document.getElementById('fileInput').files[0]
        console.log(file)
        console.log($scope.expDate)
        if(!file) {
            $scope.errorText = "Please select a file to upload"
            return 
        }
        if(!$scope.expDate) {
            $scope.errorText = "Please select an expiration date"
            return 
        }
        $http({
            method: 'POST',
            url: '/file/upload',
            headers: {'Content-Type': undefined},
            transformRequest: data => {
                let formData = new FormData()
                formData.append("model", angular.toJson(data.model))
                formData.append("file", data.file)
                return formData
            },
            data: {
                model: {
                    expDate: $scope.expDate,
                    name: file.name,
                    type: file.type.split('/')[1],
                    ownerID: $scope.user.username,
                },
                file: file
            }
        })
            .then(res => {
                console.log(res)
                if(res.data.status == "200") {
                    let newFile = {
                        expDate: $scope.expDate,
                        name: file.name,
                        type: file.type.split('/')[1],
                        id: res.data.id
                    }
                    $scope.user.files.push(newFile)
                    sessionStorage.setItem('currentUser', JSON.stringify($scope.user))
                    window.location = '/dashboard'
                }
            })
    }
}])