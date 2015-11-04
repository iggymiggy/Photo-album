$(document).on('submit', '.ajax-form', function(form) {
  form.preventDefault();
  $.ajax({
    type: $(this).attr('method'),
    url: $(this).attr('action'),
    data: $(this).serialize(),
    async: false,
    success: function(data) {
      if (!(data['success'])) {
        //alert(data); //temporary solution
      } else {
        document.location.reload(); //I hate doing it like this
      }
    }
  });
  
  //Submit create album form
  $(".create-album-btn").click(function(){
    $.ajax({
      url: url,
      type: "POST",
      dataType: "html",
      success: function(data) {
        //alert(data);
      }
    });
  });
});
