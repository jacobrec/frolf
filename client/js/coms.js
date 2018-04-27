const server = "http://localhost:8888";
function get(path, callback){
    var myRequest = new XMLHttpRequest();
    myRequest.open('GET', server+path);
    myRequest.onreadystatechange = function () {
        if (myRequest.readyState === 4) {
            callback(myRequest.responseText);
        }
    };
    myRequest.send();
}