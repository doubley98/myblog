var vm = new Vue({
        el: "#app",
        delimiters: ['[[', ']]'],
        data: {
            host: "http://182.92.219.208:9000",
            error_name: false,
            error_password: false,
            error_name_message: '请输入5-20个字符的用户',
            error_password_message: '请输入8-20位的密码',
            username: "",
            password: "",
            remember: false
        },
        methods: {
            check_username() {
                var re_username = /^[a-zA-Z0-9_-]{5,20}$/;
                var re_mobile = /^1[345789]\d{9}$/;
                if (re_mobile.test(this.username)) {
                    this.error_name = false
                } else if (re_username.test(this.username)) {
                    this.error_name = false
                } else {
                    this.error_name_message = '请正确输入用户名';
                    this.error_name = true
                }
            },
            check_password() {
                var re = /^[0-9A-Za-z]{8,20}$/;
                if (re.test(this.password)) {
                    this.error_password = false;
                } else {
                    this.error_password = true;
                    this.error_password_message = '请输入8-20位的密码';
                }
            },
            check_all() {
                this.check_username();
                this.check_password();
            },
            on_submit() {
                this.check_all();
                if (this.error_name !== true && this.error_password !== true) {
                    axios.post(this.host + "/login/", JSON.stringify({
                        "username": this.username,
                        "password": this.password,
                        "remember": this.remember
                    })).then(response => {
                        if (response.data.status !== 200) {
                            this.error_password = true;
                            this.error_password_message = response.data.msg
                        } else {
                            this.username = "";
                            this.password = "";
                            this.remember = false;
                            window.location = "/blogList/"
                        }
                    }).catch(error => {
                        console.log(error)
                    })
                }
            }
        }
    })