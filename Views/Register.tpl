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
 form {   
        border: 3px solid #f1f1f1;   
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
        <center> <h1> Register </h1> </center> 
    % elif user_exists:
        <center> <h1 class="textfont"> {{user}} already exists!! Enter a different username </h1> </center>
    % else:
        <center> <h1 class="textfont"> Passwords do not match. Register again!! </h1> </center> 
    % end
    <form method="post">  
        <div class="container">   
            <label>Username (Enter 4-8 characters) </label>   
            <input type="text" placeholder="Enter Username" name="username" pattern="[a-zA-Z]{4,8}" required>  
            <label>First name </label>   
            <input type="text" placeholder="Enter first name" name="firstname" required> 
            <label>Last name </label>   
            <input type="text" placeholder="Enter last name" name="lastname" required> 
            <label>Password (Enter at least 8 characters. Must contain at least 1 lowercase, uppercase character and a number) </label>   
            <input type="password" placeholder="Enter Password" name="password_1" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" required>
            <label>ReEnter Password : </label>   
            <input type="password" placeholder="ReEnter Password" name="password_2" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" required>
            <button type="submit">Register</button>  
        </div>   
    </form>  
</body>     
</html>