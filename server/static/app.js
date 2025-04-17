let app = angular.module("MyApp", [])
let baseURL = window.env?.baseURL

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
        if($scope.username.indexOf('@') != -1) {
            $scope.errorText = "Usernames cannot contain the @ character"
            return 
        }
        if($scope.email.length == 0) {
            $scope.errorText = "email is required"
            return
        }
        if($scope.email.indexOf('@') == -1) {
            $scope.errorText = "Please enter a valid email"
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
        $http.post(`${baseURL}/filedrop-user-signup`, data)
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
        $http.post(`${baseURL}/filedrop-user-login`, data)
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

app.controller("dashboardCtrl", ['$scope', '$http', function($scope, $http) {
    $scope.logout = () => {
        console.log('logout')
        sessionStorage.removeItem('currentUser')
        window.location = '/'
    }
    $scope.user = JSON.parse(sessionStorage.getItem('currentUser'))
    $scope.files = $scope.user.files.map(file => JSON.parse(file))
    $scope.deleteFile = (id, name) => {
        if(confirm(`Delete ${name} from our servers? (This action cannot be undone)`)) {
            let data = {
                displayID: id
            }

            $http.post(`${baseURL}/filedrop-file-delete`, data)
                .then(res => {
                    $scope.files = $scope.files.filter(file => file.displayID != id)
                    $scope.user.files = [...$scope.files].map(file => JSON.stringify(file))
                    sessionStorage.setItem('currentUser', JSON.stringify($scope.user))
                    alert(res.data.message)
                })
        }
    }
    $scope.copyFileCode = id => {
        navigator.clipboard.writeText(id)
    }
    $scope.downloadFile = id => {
        let link = document.createElement('a')
        link.href = `/${id}`
        link.download = id
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
    }
    $scope.UIDateString = dateStr => {
        let date = new Date(dateStr)
        return `${date.getMonth()+1}-${date.getDate()}-${date.getFullYear()}`
    }
    $scope.scrollToRight = (event) => {
        event.target.scroll({
            left: event.target.scrollWidth,
            behavior: 'smooth'
        })
    }
    $scope.scrollBack = (event) => {
        event.target.scroll({left: 0})
    }
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
        $scope.expDate.setHours(23)
        $scope.expDate.setMinutes(59)
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
                    displayName: file.name,
                    type: file.name.split('.').slice(-1)[0],
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
                        displayName: file.name,
                        type: file.name.split('.').slice(-1)[0],
                        displayID: res.data.displayID
                    }
                    console.log(newFile)
                    $scope.user.files.push(JSON.stringify(newFile))
                    sessionStorage.setItem('currentUser', JSON.stringify($scope.user))
                    window.location = '/dashboard'
                }
            })
    }
}])