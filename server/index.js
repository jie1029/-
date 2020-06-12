var express = require("express");
var app = express();
var path  = require('path');
var bodyParser = require('body-parser');

//post body 전달을 위해 body-parser이 있어야 한다고 함
app.use(bodyParser.json());

//서버가 HTML 렌더링을 할 때, EJS 엔진을 사용하도록 설정합니다.
app.set('view engine', 'ejs');
app.engine('html', require('ejs').renderFile);

//라우터 설정
var titleGetRouter = require('./router/main');
app.use('/',titleGetRouter);

app.listen(80, function(){
    console.log("App is running on port 80");
});

