
async function send_login() {
    
  var formdata = new FormData();
  formdata.append("username", "'test'");
  formdata.append("password", "'pass'");
  
  var requestOptions = {
    method: 'POST',
    body: formdata,
    redirect: 'follow'
  };
  
  fetch("http://localhost:8000/api/token", requestOptions)
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
}

document.getElementById("auth_button").addEventListener("click", send_login)