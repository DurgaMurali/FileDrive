<!DOCTYPE html>
<html>
<style>
Body {  
  font-family: Calibri, Helvetica, sans-serif;  
  background-color: white;  
}   
  
 input[type=text]{ 
        background-color: #BCC6CC   
        width: 100%;
        color: #000000;   
        margin: 8px 0;  
        padding: 12px 20px;   
        display: inline-block;   
        border: 2px blue;   
        box-sizing: border-box;   
    }  
   input[type=submit] { 
        background-color: #007C80;   
        width: 50%;
        color: #FFFFFF;   
        margin: 8px 0;  
        padding: 12px 20px;   
        display: inline-block;   
        border: 2px blue;   
        box-sizing: border-box;   
    }    
        
     
 .container {     
        background-color: lightblue;
        margin: auto;
        width: 30%;
        padding: 10px
    } 

   .logout {
        margin: auto;     
        width: 30%;
        padding: 10px
    }

  .textfont {
  color: #307D7E;
  font-family=Calibri
  }  

  .subtextfont {
  color: #4C787E;
  font-family=sans-serif
  } 

  .inputtextfont {
  font-weight: bold;
  color: #008080;
  font-family=sans-serif
  }

</style>

<body>

% if welcome:
  <center> <h1 class="textfont"> Welcome {{user}} </h1> </center>
% elif file_success:
  <center> <h1 class="textfont"> {{user}}'s Dashboard </h1> </center>
  <center> <h3 class="subtextfont"> File successfully saved to {{folder_name}} </h3> </center>
% elif file_fail:
  <center> <h1 class="textfont"> {{user}}'s Dashboard </h1> </center>
  <center> <h3 class="subtextfont"> {{error_message}}! </h3> </center>
% elif folder_success:
  <center> <h1 class="textfont"> {{user}}'s Dashboard </h1> </center>
  <center> <h3 class="subtextfont"> Folder successfully created at {{folder_name}} </h3> </center>
% elif folder_fail:
  <center> <h1 class="textfont"> {{user}}'s Dashboard </h1> </center>
  <center> <h3 class="subtextfont"> {{error_message}}! </h3> </center>
% elif delete_success:
  <center> <h1 class="textfont"> {{user}}'s Dashboard </h1> </center>
  <center> <h3 class="subtextfont"> File deleted from {{folder_name}} </h3> </center>
% elif delete_fail:
  <center> <h1 class="textfont"> {{user}}'s Dashboard </h1> </center>
  <center> <h3 class="subtextfont"> {{error_message}}! </h3> </center>
%end
<br>

<form action = "/upload/{{user}}" method="POST" enctype="multipart/form-data">
  <div class="container"> 
    <text class="inputtextfont"> Select a file: </text> <input type="file" name="upload" required/> 
    <input type="submit" value="Start upload" />
  </div>
</form>
<br>

<form action = "/newfolder/{{user}}" method="POST">
  <div class="container"> 
    <text class="inputtextfont"> Folder Name: </text> <input type="text" name="folder" required/>
    <input type="submit" value="Create New Folder" />
  </div>
</form>
<br>

<form action = "/delete/{{user}}" method="POST" enctype="multipart/form-data">
  <div class="container"> 
    <text class="inputtextfont"> Filename: </text> <input type="text" name="filename" required/>
    <input type="submit" value="Delete File" />
  </div>
</form>
<br>

<form action = "/logout/{{user}}" method="POST">
  <div class="logout">
    <input type="submit" value="Logout" />
  <div class="logout">
</form>

</body>
</html>