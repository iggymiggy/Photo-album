var GET_IMAGE = 100 //how many times tries to get given image url
var img_id = "";
var img_src = STATIC_URL + "img/add_img.png";

$(document).ready(function() {
  $('.page-layout').click(function(){ //Create a new page with layout
    var layout = $(this).attr('id');
    var album_id = $(this).data('album');
    var page_name = $('#pageNameCreated').val();
    
    $('#pageNameCreated').html('');
    $('.move-left-btn').css('display', 'inline');
    $('.move-right-btn').css('display', 'inline');
    $('.remove-page-btn').css('display', 'inline');
    $('.name-page-btn').css('display', 'inline');

    //console.log($(this));
    $.ajax({
      type: 'POST',
      url: '/album/page/create/',
      data: {"layout": layout,"album_id":album_id, 'page_name':page_name,"url":(STATIC_URL + "img/add_img.png"), csrfmiddlewaretoken: $.cookie('csrftoken')},
      success: function(data) {
        $('#albumPageLayout').html(data);
        $('#layoutModal').modal('hide');
        $(".modal-backdrop").hide();
        var page_id = $('.layout').data('pageid');
        var page_number = $('.layout').data('page');
        //console.log("number: ", page_number);
         var url ="/album/view/"+album_id.toString()+"/";
         $.ajax({
            type: 'POST',
            url: url,
            data: {'page_id':page_id, 'album_id':album_id,csrfmiddlewaretoken: $.cookie('csrftoken')}, // TODO 
            success: function(data) {
            var $result = $(data).filter('#containerAlbum');
            var txt = $('#containerAlbum').html(); 
            //alert(txt);
            //console.log($result);
            //$('#containerAlbum').html('');
            $('#containerAlbum').html($result);
            //album-links remove:
            var l = "currentPage"+page_id;
            $('.slideshow-link').attr('id',l); //refresh current page to slideshow link
            $('.album-view-links').addClass('hidden');
            document.getElementById("page-name-form").reset();
          }
        });
        $('#albumPageLayout').html(data);
        
        var page_id = $('#albumPageLayout .layout').data('pageid');
        var url ="/album/view/"+album_id.toString()+"/";
         //console.log("album_id: ", album_id);
         
        var link_id= $('.view-page-link').attr('id');
        var linkIdInt = link_id.match(/\d+$/)[0]; // getting only the number of id
        $('.slideshow-link').attr('id',"currentPage"+linkIdInt); //refresh current page to slideshow link
      }
    });
    return false;
  });
});

//function for clicking image to save its id
function ImageClick(id)
{
    
  if (!$('#namePageModal').hasClass('in')){
        //show link to image
        var src = document.getElementById(id).src;
        if ( src.search(img_src)==-1){
        document.getElementById("imgLink").value= document.getElementById(id).src;
        //if not choosed any image yet, empty link box
        }else{
        document.getElementById("imgLink").value ="";
        }
        img_id = id;
  }
}

$( document ).ready(function() {
    
  //epmty form for link and flickr search
  document.getElementById("link_form").reset();
  document.getElementById("flickr_form").reset();
  //add images as link
  if (!$('#namePageModal').hasClass('in')){
    var album_id = $('.add-image-modal').data('albumid');
    $(".addImage-btn").click(function(){
        var inputti = document.getElementById("imgLink");
        var url = inputti.value
        var img = new Image();
        img.src = url;
        //Check the link validity
        if(url==""){ // if epmty string do nothing
        }
        else{ //tries to get image from url several times
            var succes = 0;
            for(var i=0; i<GET_IMAGE; i++){
                if (img.complete ) { // if valid image link, clear error area
                document.getElementById("addImageModalError").innerHTML="";
                document.getElementById("addImageModalError").setAttribute("style","display:none; text-align:left;")
                document.getElementById(img_id).src=inputti.value;
                $('#addImageModal').modal('hide');
                document.getElementById("flickrContent").innerHTML="";
                document.getElementById("flickr_form").reset();
                succes = 1;
                break;
                }
            }
             if(succes ===0){
                // if link given not valid, show error message
                document.getElementById("addImageModalError").innerHTML="Error loading url:<br>" + url;
                document.getElementById("addImageModalError").setAttribute("style","display:block; text-align:left;")
             }
        }	
        //clear forms, error areas and flickr images when closed
        $(".closeButton").click(function(){
        document.getElementById("addImageModalError").innerHTML="";
        document.getElementById("addImageModalError").setAttribute("style","display:none; text-align:left;");
        //if not added image link
        if (document.getElementById("imgLink").value == ""){
          document.getElementById(img_id).src=img_src;
        }else{
          document.getElementById("link_form").reset();
          document.getElementById("flickrContent").innerHTML="";
          $('#flickrContent').empty();
          document.getElementById("flickr_form").reset();
        }
        
      
        
        });
          //saving the page
        var page_id = $('.layout').data('pageid');
        var imgsrc = {}; // dictionary to post as json
        var layout = $('.layout').attr('id');
        var price = $('#imagePriceInModal').val();
        
        ////console.log("a: ",album_id);
        // get data for json:

        imgsrc['page_id']=page_id;
        imgsrc[img_id] = url;
        imgsrc['layout'] = layout;
        imgsrc['one_picture'] = "one_picture";
        
        imgsrc['price']=parseFloat(price);
        
        
        //alert(JSON.stringify(imgsrc));
         //call ajax
        $.ajax({
          type: 'POST',
          url: '/album/page/save/',
          data: {'data':JSON.stringify(imgsrc), csrfmiddlewaretoken: $.cookie('csrftoken')}, // TODO 
          success: function(data) {
           
             $('#albumPageLayout').html(data);
             var url ="/album/view/"+album_id.toString()+"/";
             //console.log("album_id: ", album_id);
             $.ajax({
              type: 'POST',
              url: url,
              data: {'page_id':page_id, 'album_id':album_id,csrfmiddlewaretoken: $.cookie('csrftoken')}, // TODO 
              success: function(data) {
                var $result = $(data).filter('#containerAlbum');
                var txt = $('#containerAlbum').html(); 
                //console.log($result);
                
                 //$('#containerAlbum').html('');
                  $('#containerAlbum').html($result);
                 $('.album-view-links').addClass('hidden');
                 var l = "currentPage"+page_id;
                $('.slideshow-link').attr('id',l); //refresh current page to slideshow link
                document.getElementById("picture-price-form").reset();
              }
            });
          }
        });
        
        
      });
    }
});
