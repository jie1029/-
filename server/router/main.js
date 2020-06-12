
var express = require('express');
var router = express.Router();
var {PythonShell} = require('python-shell');
var bodyParser = require('body-parser');
var multer = require('multer');

var storage = multer.diskStorage({
    destination:function(req,file,callback){
        callback(null,"./demo/upload/")
    },
    filename:function(req,file,callback){
        callback(null,file.originalname)
    }
});

var upload = multer({
    storage:storage
});

router.use(bodyParser.json());

router.use((req,res,next)=>{
    // 해당미들웨어의 config가 위치한뒤 next()로 다음 미들웨어로 넘어가도록 처리한다.
    console.log('new request', req.method, req.path, new Date().toLocaleTimeString());
    next();
});

router.get('/',function(req,res){
    res.render('description.html');
});

router.get('/file',(req,res) => {
    res.render('inputCSV.html');
});

router.get('/text',(req,res) => {
    res.render('inputText.html');
});

router.get('/loding',(req,res)=>{
    res.sendfile("./images/Spinner-1s-200px.gif");
});

router.post('/upload',upload.single("csvFile"),(req,res) => {
    var file = req.file

    var options = {
        mode: 'text',
        pythonPath: '/home/mls-server/anaconda3/envs/server/bin/python',
        pythonOptions: ['-u'],
        scriptPath: '',
        args: [file.originalname]
    }

    PythonShell.run('demo/csvLoad.py',options,function(err,results){
        if (err) throw err;
        result = JSON.parse(results[results.length-1]);
        res.download("./demo/result/"+result.file_name,result.file_name);
    })

});

router.post('/titleGenerate',function(req,res){

    var options = {

        mode: 'text', 
        pythonPath: '/home/mls-server/anaconda3/envs/server/bin/python',
        pythonOptions: ['-u'],
        scriptPath: '',
        args: [req.body.inputText]
      
    }

    PythonShell.run('demo/test.py',options,function(err,results){
        if (err) throw err;
        res.json({data:results[results.length-1]});              
    })

    
    // 
});

module.exports = router;
