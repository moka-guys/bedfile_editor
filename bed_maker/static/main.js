
$(document).ready(function () {

    $("#manual-upload-form").submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/manual_import/",
            data: $("#manual-upload-form").serialize(),
            beforeSend: function () {
                $("#p1").append('<div id="spinner-circle" class="text-center mt-3"><div class="spinner-border text-primary" role="status"></div><h3>LOADING!</h3></div>');
            },
            success: function (response) {
                //alert(response);

                $("#spinner-circle").remove();
                $("#p1").append('<div class="alert alert-success" role="alert";"><strong><h3> Gene list was uploaded successfully!</strong></h3></div>');

                // $(".post_submitting").fadeOut(1000);
            }
        });
        e.preventDefault();
    });


});



//$.ajax ({
 //   type: 'GET',
 //   url: 'manual_import/',
  //  success: function(response){
  //      spinnerCircle.classList.remove('not-visible')
 //       console.log('response', response)
//    },
 //   error: function(error) {
  //      console.log(error)
 //   }
//})