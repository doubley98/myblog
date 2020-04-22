var vm = new Vue({
        el: "#app",
        delimiters:["[[","]]"],
        data: {
            username:"",
            host: "http://182.92.219.208:9000",
            // 假设这是后台传来的数据来源
            information:{{ information|safe }},
        },
        methods: {
            getUsername() {
                var strCookie = document.cookie;
                var arrCookie = strCookie.split("; ");
                for (var i = 0; i < arrCookie.length; i++) {
                    var arr = arrCookie[i].split("=");
                    //找到名称为userId的cookie，并返回它的值
                    if ("username" == arr[0]) {
                        this.username = arr[1];
                        break;
                    }
                }
            }
        },
        mounted() {
            this.getUsername()
        },
    })