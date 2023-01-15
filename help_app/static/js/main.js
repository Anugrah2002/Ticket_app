function showPassword() {
  var x = document.getElementById("password");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

function validateEmail(){
    let emailAddress = document.getElementById('email').value;
    myArray = emailAddress.split("@");
    if (myArray[1] != null){
        if (myArray[1].toLowerCase() == "vitbhopal.ac.in" ){
            document.getElementById("message").innerHTML = ""
            $.ajax({
                type:'POST',
                url:'/send_OTP/',
                data:{
                    email:emailAddress,
                    csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
                },
                success:function(data){
                    if (data == "send"){
                        document.getElementById('otpRow').hidden = false;
                        document.getElementById('otpButtonRow').hidden = false;
                        document.getElementById('validate-button').hidden = true;
                        document.getElementById("resend-button").disabled=true;
                        var sec         = 120,
                            countDiv    = document.getElementById("resend-button"),
                            countDown   = setInterval(function () {
                                'use strict';
                                secpass();
                            }, 1000);
                    function secpass() {
                        'use strict';
                            var min     = Math.floor(sec / 60),
                                remSec  = sec % 60;

                            if (remSec < 10) {
                                remSec = '0' + remSec;
                            }
                            if (min < 10) {
                                min = '0' + min;
                            }
                            countDiv.innerHTML = min + ":" + remSec;
                            if (sec > 0) {
                                sec = sec - 1;
                            } else {
                                clearInterval(countDown);
                                countDiv.disabled = false;
                                countDiv.innerHTML = 'Resend OTP';
                            }
                        }
                    }
                }
            });
        }
        else{
            document.getElementById("message").innerHTML = "Email should have @vitbhopal.ac.in"
        }
    }
    else{
         document.getElementById("message").innerHTML = "Email should have @vitbhopal.ac.in"
    }
}

function verifyOTP(){
    otp = document.getElementById('otp').value;
    let emailAddress = document.getElementById('email').value;
    $.ajax({
        type:'POST',
        url:'/verify_OTP/',
        data:{
            otp:otp,
            email:emailAddress,
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
        },
        success:function(data){
            if (data == "verified"){
                document.getElementById('otpRow').hidden = true;
                document.getElementById('otpButtonRow').hidden = true;
                verifiedFrom = document.getElementsByClassName("verifiedFrom");
                for(i=0;i<verifiedFrom.length;i++){
                    verifiedFrom[i].hidden = false;
                }
            }
            else if (data == "not verified"){
                document.getElementById("otp-text").innerHTML = "Please Enter the correct OTP!";
                document.getElementById("otp-text").style.color = "red";
            }
        }
    });
}

function submitForm(){
    document.getElementById('complainForm').submit()
}