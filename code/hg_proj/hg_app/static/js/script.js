$(document).ready(function () {

  $("#12345").click(function () {
    $(this).hide("slow");
  });

  
var audio = document.getElementsByClassName("bgMusic")[0];
audio.volume = 0.1;
audio.autoplay = true;


  

});



function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      $("#img-preview").attr("src", e.target.result);
    };

    reader.readAsDataURL(input.files[0]); // convert to base64 string
  }
}

$("#file-upload").change(function () {
  readURL(this);
});