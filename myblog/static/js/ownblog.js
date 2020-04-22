var vm = new Vue({
        el: "#app",
        delimiters: ['[[', ']]'],
        data: {
            keyword: "",
            username: "",
            host: "http://182.92.219.208:9000",
            // 假设这是后台传来的数据来源
            data: {{ blogList|safe }},
            // 所有页面的数据
            totalPage: [],
            // 每页显示数量
            pageSize: 10,
            // 共几页
            pageNum: 0,
            // 当前显示的数据
            dataShow: "",
            // 默认当前显示第一页
            currentPage: 0
        },
        methods: {
            nextPage() {
                if (this.currentPage === this.pageNum - 1) return;
                this.dataShow = this.totalPage[++this.currentPage];
            },
            lastPage() {
                if (this.currentPage === 0) return;
                this.dataShow = this.totalPage[--this.currentPage];
            },
            //分页实现
            paging() {
                this.pageNum = Math.ceil(this.data.length, 5);
                for (i = 0; i < this.pageNum; i++) {
                    // totalPage是一个临时的存储容器，用来进行数据的切分
                    this.totalPage[i] = this.data.slice(this.pageSize * i, this.pageSize * (i + 1))
                }
                this.dataShow = this.totalPage[this.currentPage];
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
            }
        },
        mounted() {
            this.getUsername()
            this.paging()
        },
    })