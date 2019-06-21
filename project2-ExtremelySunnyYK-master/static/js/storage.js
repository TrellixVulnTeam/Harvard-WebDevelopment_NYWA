//localStorage

function handleSubmit(){
    username = document.getElementById("name").value;
    password = document.getElementById("pass").value;

    localStorage.setItem(username,password);
    console.log(username,password);
    console.log('success');
    }


function checkInformation(){
    username = document.getElementById("your_name").value;
    password = document.getElementById("your_pass").value;

    if (localStorage.getItem(username) == password){
        alert("success");

    }
    else{
    alert("Invalid username or password")
    return false
    }

   }

//function createChannel{
//}
