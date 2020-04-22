var vm = new Vue({
        el: "#app",
        delimiters: ['[[', ']]'],
        data: {
            host: "http://182.92.219.208:9000",
            error_name: false,
            error_password: false,
            error_phone: false,
            error_image_code: false,
            error_allow: false,
            error_name_message: '请输入5-20个字符的用户',
            error_password_message: '请输入8-20位的密码',
            error_mobile_message: '请输入正确的手机号码',
            error_image_code_message: '请填写图形验证码',
            error_allow_message: '请勾选用户协议',
            username: "",
            password: "",
            mobile: "",
            image_code: "",
            allow: false,
            register_message: "",
            image_code_id: '',
            image_code_url: '',
        },
        methods: {
            // 生成唯一标识符uuid
            generateUUID() {
                var d = new Date().getTime();
                if (window.performance && typeof window.performance.now === "function") {
                    d += performance.now(); //use high-precision timer if available
                }
                var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
                    var r = (d + Math.random() * 16) % 16 | 0;
                    d = Math.floor(d / 16);
                    return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
                });
                return uuid;
            },
            // 发起请求 请求图片验证码
            generate_image_code() {
                // 生成一个编号 : 严格一点的使用uuid保证编号唯一， 不是很严谨的情况下，也可以使用时间戳
                this.image_code_id = this.generateUUID();
                // 设置页面中图片验证码img标签的src属性
                this.image_code_url = this.host + "/image_codes/" + this.image_code_id + "/";
                console.log(this.image_code_url);
            },
            check_username() {
                var re = /^[a-zA-Z0-9_-]{5,20}$/
                if (re.test(this.username)) {
                    this.error_name = false
                } else {
                    this.error_name_message = '请输入5-20个字符的用户名';
                    this.error_name = true
                }
                if (!this.error_name) {
                    axios.get(this.host + "/username/" + this.username + "/count/").then(response => {
                        if (response.data.count > 0) {
                            this.error_name_message = "已存在的用户名";
                            this.error_name = true
                        }
                    }).catch(error => {
                        console.log(error)
                    })
                }

            },
            check_mobile() {
                var re = /^1[345789]\d{9}$/;
                if (re.test(this.mobile)) {
                    this.error_phone = false;
                } else {
                    this.error_mobile_message = '您输入的手机号格式不正确';
                    this.error_phone = true;
                }
                if (!this.error_phone) {
                    axios.get(this.host + "/mobile/" + this.mobile + "/count/").then(response => {
                        if (response.data.count > 0) {
                            this.error_mobile_message = "已存在的手机号";
                            this.error_phone = true
                        }
                    }).catch(error => {
                        console.log(error)
                    })
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
            check_image_code() {
                if (!this.image_code) {
                    this.error_image_code_message = '请填写图片验证码';
                    this.error_image_code = true;
                } else {
                    this.error_image_code = false;
                }
                axios.post(this.host + "/check_image_codes/", JSON.stringify({
                    "image_code": this.image_code,
                    "image_code_id": this.image_code_id
                }), {
                    responseType: 'json'
                }).then(response => {
                    if (response.data.status !== 200) {
                        this.error_image_code_message = response.data.msg;
                        this.error_image_code = true
                    }
                }).catch(error => {
                    console.log(error)
                })
            },
            check_allow() {
                if (!this.allow) {
                    this.error_allow = true;
                } else {
                    this.error_allow = false;
                }
            },
            check_all() {
                this.check_username();
                this.check_mobile();
                this.check_password();
                this.check_image_code();
                this.check_allow();
            },
            on_submit() {
                this.check_all();

                if (this.error_name !== true && this.error_password !== true && this.error_phone !== true && this
                    .error_allow !== true && this.error_image_code !== true) {
                    axios.post(this.host + "/register/", JSON.stringify({
                        "username": this.username,
                        "password": this.password,
                        "mobile": this.mobile,
                        "allow": this.allow
                    })).then(response => {
                        if (response.data.status !== 200) {
                            alert(response.data.msg)
                        } else {
                            alert(response.data.msg);
                            window.location = '/login/'
                        }
                    }).catch(error => {
                        console.log(error)
                    })
                }
            }
        },
        mounted() {
            this.generate_image_code()
        },
    })