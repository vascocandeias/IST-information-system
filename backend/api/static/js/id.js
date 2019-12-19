function getSecret() {
    console.log("button pressed");
    document.getElementById("secret").innerHTML = "HEY";
}

document.getElementById('getSecretBtn').onclick = function () {
    jQuery.post("/mobile/secret", {"secret":sessionStorage.getItem("secret")}, function(data, status){
        document.getElementById("secret").innerHTML = data.secret;
    }, 'json')
};

document.getElementById('Submit').onclick = function () {
    console.log("getting user information");
    jQuery.getJSON("/mobile/secret", {"secret":document.getElementById("otherSecret").value}, function(data, status){
        // document.getElementById("secret").innerHTML = data.secret;
        console.log("success");
    })
};