document.getElementById('getSecretBtn').onclick = function () {
    jQuery.post("/mobile/secret", function(data){
        document.getElementById("secret").innerHTML = data.secret;
        clearInterval(ping);
        ping = setInterval(callback, 500, data.secret);
    }, 'json')
};

document.getElementById('Submit').onclick = function () {
    jQuery.getJSON("/mobile/secret", {
            "secret":document.getElementById("otherSecret").value,
        }, function(data){
            document.getElementById("d1").innerHTML = `
            <img src="data:${data.photo.type};base64, ${data.photo.data}" alt="Student Photo"> <br> 
            Name: ${data.name} <br>
            IST-id: ${data.istid} <br><br>  
        `;
    }).fail(function(){
        document.getElementById("d1").innerHTML = "User not found";
    })
};

var ping;

function callback(secret) {
    jQuery.getJSON("/mobile/requests/" + secret, function(data, status) {
        clearInterval(ping);
        document.getElementById("secret").innerHTML = "";
        document.getElementById("d1").innerHTML = `
            Your identification was requested by: <br><br>
            <img src="data:${data.photo.type};base64, ${data.photo.data}" alt="Student Photo"> <br> 
            Name: ${data.name} <br>
            IST-id: ${data.istid} <br><br>  
        `;
    }).fail(function(event) {
        if(event.status == 410) {
            clearInterval(ping);
            document.getElementById("secret").innerHTML = "";
            document.getElementById("d1").innerHTML = "Your secret is no longer valid, request a new one";
        }
    })

}