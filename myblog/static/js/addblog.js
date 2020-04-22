var vm = new Vue({
        el: "#app",
        data: {
            host: "http://182.92.219.208:9000",
            title: "",
            content: "",
            content_length: 0,
            error_title: false,
            error_content: false,
            error_title_message: "文章标题不能为空",
            error_content_message: "请填写文章内容",
        },
        methods: {
            length() {
                this.content_length = this.content.length
            },
            check_title() {
                if (this.title.length > 30) {
                    this.error_title_message = "标题长度限制在30个字符内";
                    this.error_title = true
                } else if (this.title.length <= 0) {
                    this.error_title = true
                } else {
                    this.error_title = false
                }
            },
            check_content() {
                if (this.content_length > 10000) {
                    this.error_content_message = "文章长度限制在10000个字符内";
                    this.error_content = true
                } else if (this.content_length <= 0) {
                    this.error_content = true
                } else {
                    this.error_content = false
                }
            },
            check_all() {
                this.check_title();
                this.check_content();
            },
            on_submit() {
                this.check_all();
                if (this.error_content !== true && this.error_title !== true) {
                    axios.post(this.host + "/addBlog/", JSON.stringify({
                        "title": this.title,
                        "content": this.content
                    })).then(response => {
                        if (response.data.status !== 200) {
                            alert(response.data.msg)
                        }
                        this.title = "";
                        this.content = "";
                        window.location = "/blogList/";
                    }).catch(error => {
                        console.log(error)
                    })
                }
            }
        }
    })