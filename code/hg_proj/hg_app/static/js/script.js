var audio = document.getElementById("bgMusic"); 
audio.volume = 0.1;
audio.autoplay = true


var ImgPreview = document.getElementById("img-preview");
var fileUpload = document.getElementById("file-upload");
$("#file-upload").submit(function (e) {
  e.preventDefault();
  $.ajax({
    url: "upload",
    method: "POST",
    data: $(this).serialize(),
    success: function (serverResponse) {
      console.log("before the html update");
      $(".notes-div").html(serverResponse);
        console.log("i think i made changes");
        var success = document.getElementById("success");
        success.innerHTML = "<p>Thank you! Your video has been uploaded!</p>";
    },
  });
  $(this).trigger("reset");
});


function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      $("#blah").attr("src", e.target.result);
    };

    reader.readAsDataURL(input.files[0]); // convert to base64 string
  }
}

$("#imgInp").change(function () {
  readURL(this);
});