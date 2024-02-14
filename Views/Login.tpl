<!DOCTYPE html>   
<html>   
<head>  
<meta name="viewport" content="width=device-width, initial-scale=1">  
<title> Login Page </title>  
<style>   
Body {  
  font-family: Calibri, Helvetica, sans-serif;  
  background-color: white;  
}  
button {   
       background-color: #008CBA;   
       width: 100%;  
        color: #FFFFFF;   
        padding: 15px;   
        margin: 10px 0px;   
        border: none;   
        cursor: pointer;   
         }     
 input[type=text], input[type=password] {   
        width: 100%;   
        margin: 8px 0;  
        padding: 12px 20px;   
        display: inline-block;   
        border: 2px blue;   
        box-sizing: border-box;   
    }  
 button:hover {   
        opacity: 0.7;   
    }   
  .registerbtn {   
        width: auto;   
        padding: 10px 18px;  
        margin: 10px 5px;  
    }   
        
     
 .container {   
        padding: 25px;   
        background-color: lightblue;  
        margin: auto;
        width: 50%;
        padding: 10px
    }

 .textfont {
    color: #38ACEC;
    font-family=Calibri
 }
   
</style>   
</head>    
<body> 
    % if register:
        <center> <h1 class="textfont"> Incorrect username or password! </h1> </center>
    % elif retry:
        <center> <h1 class="textfont"> Incorrect username or password! Retry </h1> </center>
    % elif register_success:
        <center> <h1 class="textfont"> Registered Successfully! Login </h1> </center>
    % elif logout:
        <center> <h1 class="textfont"> Logged out! Login Again? </h1> </center>
    % else:  
        <center> <h1 class="textfont"> Login </h1> </center>
    % end 

    <form action="/login" method="post">  
        <div class="container">   
            <label>Username : </label>   
            <input type="text" placeholder="Enter Username" name="username" required>  
            <label>Password : </label>   
            <input type="password" placeholder="Enter Password" name="password" required>  
            <button type="submit">Login</button>  
        </div>   
    </form>
    
    <form action = "/register">
        <div class="container"> 
            New User?   
            <button type="submit" class="registerbtn"> Register </button> 
        </div>
    </form>  
</body>     
</html>