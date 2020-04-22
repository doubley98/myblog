var vm = new Vue({
        el: "#app",
        delimiters: ['[[', ']]'],
        data: {
            host: "http://182.92.219.208:9000",
            mycomment: "",
            blog: {{ blogList|safe }},
            comments: [],
            error_comment_message: "评论内容不能为空",
            error_comment: false,
        },
        methods: {
            getComments() {
                url = window.location.href;
                blogId = url.substring(url.lastIndexOf('/') + 1, url.length);
                axios.get(this.host + "/getComments/" + blogId).then(response => {
                    if (response.data.status !== 200) {
                        alert(response.data.msg)
                    } else {
                        this.comments = response.data.commentList
                    }
                })
            },
            getUsername() {
                var strCookie = document.cookie;
                var arrCookie = strCookie.split("; ");
                for (var i = 0; i < arrCookie.length; i++) {
                    var arr = arrCookie[i].split("=");
                    //找到名称为userId的cookie，并返回它的值
                    if ("username" === arr[0]) {
                        this.username = arr[1];
                        break;
                    }
                }
            },
            check_comment() {
                if (this.mycomment.length === 0) {
                    this.error_comment = true
                } else {
                    this.error_comment = false
                }
            },
            on_submit() {
                this.check_comment();
                if (this.error_comment !== true) {
                    url = window.location.href;
                    blogId = url.substring(url.lastIndexOf('/') + 1, url.length);
                    axios.post(this.host + "/addComment/", JSON.stringify({
                        "comment": this.mycomment,
                        "blogId": blogId
                    })).then(response => {
                        if (response.data.status !== 200) {
                            alert(response.data.msg)
                        } else {
                            alert("评论成功");
                            this.mycomment = "";
                            this.getComments()
                        }
                    }).catch(error => {
                        console.log(error)
                    })
                }
            },
        },
        mounted() {
            this.getUsername();
            this.getComments()
        },
    })