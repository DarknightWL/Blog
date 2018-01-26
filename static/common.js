/**
 * Created by Darknight on 2017/12/27.
 */
function login(){
    login_shit = window.open("login", "login", "toolbar=no, left=300, top=200, menubar=no, width=260, height=200, location=no");
}
function checkForm(){
    var ulogin_pwd = document.getElementById('uloginpwd');
    var login_pwd = document.getElementById('loginpwd');
    login_pwd.value = ulogin_pwd.value;
    return true;
}