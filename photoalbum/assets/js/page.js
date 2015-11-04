function ShowAlbums(){
    window.location = '/';
}
//
function MoveLeft(){
    var page_id = $('.layout').data('pageid');
    var number = $('.layout').data('page');
    var album_id = $('.layout').data('albumid');
    if (number <2) return false;
    $.ajax({
      type: 'POST',
      url: '/album/page/moveleft/',
      data: {'page_id': page_id, csrfmiddlewaretoken: $.cookie('csrftoken')},
      success: function(data) {
        $('#albumPageLayout').html(data);
        page_id = $('.layout').data('pageid');
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
    return false;
}
function MoveRight(button){
    var page_id = $('.layout').data('pageid');
    var number = $('.layout').data('page');
    var album_id = $('.layout').data('albumid');
    var length = $(button).data('length');
    if (number > length -1) return false;
    $.ajax({
      type: 'POST',
      url: '/album/page/moveright/',
      data: {'page_id': page_id, csrfmiddlewaretoken: $.cookie('csrftoken')},
      success: function(data) {
        $('#albumPageLayout').html(data);
        page_id = $('.layout').data('pageid');
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
    return false;
}
function RemovePage(input_id){
    $('#removePageModal').modal('hide');
    $(".modal-backdrop").hide();
    var page_id = $('.layout').data('pageid');
    $.ajax({
      type: 'POST',
      url: '/album/page/remove/',
      data: {'pageid': page_id, csrfmiddlewaretoken: $.cookie('csrftoken')},
      success: function(data) {
      $('body').delegate('a', 'click', function(){
            return true;
        });
         window.location.reload();
      }
    });
    return false;
}

function NamePage(namepageid){
    $('#namePageModal').modal('hide');
    $(".modal-backdrop").hide();
    var pageid = namepageid.match(/\d+$/)[0];
    var newName = $('#newPageNameValue').val();
    $.ajax({
      type: 'POST',
      url: '/album/page/name/',
      data: {'page_id':pageid, 'newName': newName, csrfmiddlewaretoken: $.cookie('csrftoken')},
      success: function(data) {
        $('body').delegate('a', 'click', function(){
            return true;
        });
        $('body').delegate('img', 'click', function(){
            return true;
        });
         $('#albumPageLayout').html(data);
      }
    });
    return false;
}
function NameAlbum(album){
    $('#renameAlbum').modal('hide');
    $(".modal-backdrop").hide();
    var albumid = $(album).data('albumid');
    var newName = $('#newAlbumName').val();
    var newDes = $('#newAlbumDescription').val();
    $.ajax({
      type: 'POST',
      url: '/album/rename/',
      data: {'newName':newName, 'newDes': newDes, 'album_id': albumid, csrfmiddlewaretoken: $.cookie('csrftoken')},
      success: function(data) {
        $('body').delegate('a', 'click', function(){
            return true;
        });
        $('body').delegate('img', 'click', function(){
            return true;
        });
         var $result = $(data).filter('#containerAlbum');
        $('#containerAlbum').html($result);
        if (!$(document).hasClass( "layout" )){
            $('.remove-page-btn').css('display', 'none');
            $('.name-page-btn').css('display', 'none');
            $('.move-left-btn').css('display', 'none');
            $('.move-right-btn').css('display', 'none');
        }
      }
    });
    return false;
}
function RemoveAlbum(input_id){
    //console.log("id: ", input_id);
    $('#removeAlbumModal').modal('hide');
    $(".modal-backdrop").hide();
    var album_id = input_id.match(/\d+$/)[0];
    $.ajax({
      type: 'POST',
      url: '/album/remove/',
      data: {'album_id':album_id, csrfmiddlewaretoken: $.cookie('csrftoken')},
      success: function(data) {
        $('body').delegate('a', 'click', function(){
            return true;
        });
        window.location.reload();
      }
    });
    return false;
    
}

function SaveCaption(textbox,caption_text, image_number, page_id,album_id ){
    var layout = $('.layout').attr('id');
    data= {};
    data['image_number'] = image_number;
    data['page_id'] = page_id;
    data['caption_text'] = caption_text;
    data['layout']=layout;
    data['album_id']=album_id;
    $.ajax({
      type: 'POST',
      url: '/album/page/save/',
      data: {'data':JSON.stringify(data), csrfmiddlewaretoken: $.cookie('csrftoken')},
      success: function(data) {
         timer = 0;
      }
    });
    timer_ready = true;
   } 

var timer_ready = true;
var timer;
//this is for saving image captions
function KeyupFunction(textbox){
    if(timer_ready == true){
        timer_ready = false;
        timer = setTimeout(function (){
            var album_id = $('#containerAlbum').data('albumid');
            var caption_text = $(textbox).val();
            var textbox_id = $(textbox).attr('id');
            var image_number = textbox_id.match(/\d+$/)[0]; // getting only the number of id
            var page_id = $(textbox).data('pageid');
             SaveCaption(textbox,caption_text, parseInt(image_number), page_id,album_id);
         }, 1000); 
    }
}

$(document).ready(function() {
 if( $('#containerAlbum').hasClass('public')){
       //console.log("public");
       $('textarea').each(function() {
            //console.log("text");
             $(this).attr('disabled','disabled');
        });
        $('.album-img').each(function() {
            //console.log("a");
             $(this).addClass('disableClick');
        });
    }
    
    $('body').delegate('a', 'click', function(){
            return true;
        });
    $('.remove-page-btn').css('display', 'none');
    $('.name-page-btn').css('display', 'none');
    $('.move-left-btn').css('display', 'none');
    $('.move-right-btn').css('display', 'none');
    
    //hide slideshow if album just created and there arw no page
    
    //disable enter key
    $('html').bind('keypress', function(e)
    {
       if(e.keyCode == 13)
       {
          return false;
       }
    });
   
     $('.albums-link').click(function(){
        alert("albums");
        //call ajax
        $.ajax({
          type: 'POST',
          url: '/',
          data: { csrfmiddlewaretoken: $.cookie('csrftoken')},
          success: function(data) {
            document.body.innerHTML = '';
            ocument.body.innerHTML = data;
            if( $('#containerAlbum').hasClass('public')){
               //console.log("public");
               $('textarea').each(function() {
                    //console.log("text");
                     $(this).attr('disabled','disabled');
                });
                $('.album-img').each(function() {
                    //console.log("a");
                     $(this).addClass('disableClick');
                });
            }
          }
        });
    });
  //disable clickng outside naming modal to prevent addImageModal to opening
  $('.name-page-btn').click(function(event){
    $('body').delegate('a', 'click', function(){
        
    });
  });
  //disable clickng outside naming modal to prevent addImageModal to opening
  $('.remove-page-btn').click(function(event){
    $('body').delegate('a', 'click', function(){
        return false;
    });
  });
   //disable clickng outside naming modal to prevent addImageModal to opening
  $('.remove-album-btn').click(function(event){
    $('body').delegate('a', 'click', function(){
        return false;
    });
  });
  
  //view page
  //this is for album_view page links
  $('.view-page-link').click(function(){
    //console.log("view page link1");
     $('.move-left-btn').css('display', 'inline');
    $('.move-right-btn').css('display', 'inline');
     $('.remove-page-btn').css('display', 'inline');
    $('.name-page-btn').css('display', 'inline');
    //event.preventDefault();
    // get data for image fields and save clicked link to variable
    var link_id= $(this).attr('id');
    //console.log("link_id: ", link_id);
    var clicked_link = $(this);
    
    //get next and previous links
    var next_id = $(this).parent().next().find("a").attr('id');
    //console.log("next_id: ", next_id);
    var prev_page = $(this).parent().prev().find("a").data('numberofpage');
    //console.log("prev_id: ", prev_id);
    if (typeof prev_page != 'undefined'){
        var prev_id = $(this).parent().prev().find("a").attr('id');
    }
    var id = link_id.match(/\d+$/)[0]; // getting only the number of id 
    //call ajax
    $.ajax({
      type: 'POST',
      url: '/album/page/view/',
      data: {'page_id': id, csrfmiddlewaretoken: $.cookie('csrftoken')}, // TODO 
      success: function(data) {
        //console.log("ajax1");
        //alert(data);
        //$('.view-page-link').css('visibility', 'hidden');
        //$('.album-view-links').hide();
      //$('.page-view-links').hide();
        //$('#albumPageLayout').html('');
        $('#albumPageLayout').html(data);
           if( $('#containerAlbum').hasClass('public')){
               //console.log("public");
               $('textarea').each(function() {
                    //console.log("text");
                     $(this).attr('disabled','disabled');
                });
                $('.album-img').each(function() {
                    //console.log("a");
                     $(this).addClass('disableClick');
                });
            }
        $('.album-view-links').addClass('hidden');
        var linkIdInt = link_id.match(/\d+$/)[0]; // getting only the number of id
        var l = "currentPage"+id;
        $('.slideshow-link').attr('id',l); //refresh current page to slideshow link
        if($(clicked_link).hasClass("hidden")){
            $.fancybox({
             beforeShow: function () {
             //console.log("has class hidden1");
                //console.log("fancybox1");
             this.title += '<div class="btn-group btn-group-justified">';
            var $links = $();
            //links.$('#a').css('visibility', 'hidden');
            $links.find('a').css('visibility','hidden');
             this.title += ' <div class="btn-group">';
             if ( typeof prev_id !== 'undefined'){
                    this.title += '<button type="button" id="prev-slide" class="btn  glyphicon glyphicon-chevron-left btn-primary" style="float:left"onclick="SlideShow('+prev_id+')">Prev page</button>';
                }  
            this.title += '</div>';
            this.title += ' <div class="btn-group">';    
            if ( typeof next_id !== 'undefined'){
                this.title += '<button type="button" id="next-slide" class="btn  glyphicon glyphicon-chevron-right btn-primary" style="float:right" onclick="SlideShow('+next_id+')">Next page</button>';
            }   
            this.title += '</div>';
            this.title += '</div>';
            },
            'content': data,
            closeBtn: true, 
            arrows: true,
            'transitionIn': 'none', 
            'transitionOut': 'none',
            'titlePosition': 'over',
            'autoScale' : true,
            openEffect : 'elastic',
            closeEffect : 'elasatic',
            helpers: {
                title: {
                    type: 'inside'
                }, 
                buttons: {} 
            },
            'onComplete': function() {
                $("#fancybox-wrap").css({'z-index':'8000'});
            },
                autoSize: true, // shouldn't be true ?
                fitToView: true,
               'transitionIn': 'none', 
            'transitionOut': 'none',
            'titlePosition': 'over',
            'titleFormat': function (title, currentArray, currentIndex, currentOpts) {
            return '<span id="fancybox-title-over">Image ' + (currentIndex + 1) + ' / ' + currentArray.length + (title.length ? ' &nbsp; ' + title : '') + '</span>';
            } 
        });
        }
      }
    });
    return false;
  });
  //remove page links from slideshow
  $(document).ajaxComplete(function(){
    if($('.page-buttons','.fancybox-inner').length != 0) {
        $('.page-buttons','.fancybox-inner').remove();
    }
    if($('.page-view-links','.fancybox-inner').length != 0) {
        $('.page-view-links','.fancybox-inner').remove();
    }
    if($('.text-area','.fancybox-inner').length != 0) {
        $('.text-area','.fancybox-inner').attr('disabled', 'true');
    }
    if($('.album-img','.fancybox-inner').length != 0) {
        $('.album-img','.fancybox-inner').attr( "onclick", null );
        $('.album-img','.fancybox-inner').parent().removeAttr('href');
    }
    });
    
});

function SlideShow(link_id){
    if($.type(link_id) === "string") {
       //its string
       //console.log("slideshow funcion: ", link_id);
        if ( typeof link_id != "currentPage0"){
            //console.log("if 1");
            var id = link_id.match(/\d+$/)[0]; // getting only the number of id
            var pageLinkId = "pageLin"+id;
            var p = "pageLink"+id;
            $('.hidden').each(function () {
                if( $(this).attr('id') === pageLinkId || $(this).attr('id') === p){
                    //console.log("click1: ", $(this));
                    $(this).click();
                    //console.log("if2");
                    return false;
                }
            });
            var link_object = document.getElementById(pageLinkId);
            //console.log("pagelinkid: ", link_object);
            $(link_object).click();
            }
            //console.log("eka if loppu");
    }else{
       //console.log("click2: ", link_id);
      $(link_id).click();
    }
    return false;
}
//this is for page_view page links
//stupid way to prevent an error: MultiValueDictKeyError at /album/page/view/"'page_id'"
//same function as below, but they didn't work in the same function, not very elegant but still works... 
//maybe someone can do this better...
function ToPage(link_clicked){
    //console.log("Topage2");
    $('.move-left-btn').css('display', 'inline');
    $('.move-right-btn').css('display', 'inline');
     $('.remove-page-btn').css('display', 'inline');
     $('.name-page-btn').css('display', 'inline');
    //event.preventDefault();
    // get data for image fields and save clicked link to variable
    var link_id= $(link_clicked).attr('id');
    var clicked_link = $(link_clicked);
    
    //get next and previous links
    var next_id = $(link_clicked).parent().next().find("a").attr('id');
    var prev_page = $(link_clicked).parent().prev().find("a").data('numberofpage');
    if (typeof prev_page != 'undefined'){
        var prev_id = $(link_clicked).parent().prev().find("a").attr('id');
    }
    var id = link_id.match(/\d+$/)[0]; // getting only the number of id 
    //call ajax
    $.ajax({
      type: 'POST',
      url: '/album/page/view/',
      data: {'page_id': id, csrfmiddlewaretoken: $.cookie('csrftoken')}, // TODO 
      success: function(data) {
      //console.log("ajax succes2");
      $('.album-view-links').hide();
      $('.page-view-links').show();
       $('#albumPageLayout').html('');
        $('#albumPageLayout').html(data);
        if( $('#containerAlbum').hasClass('public')){
               //console.log("public");
               $('textarea').each(function() {
                    //console.log("text");
                     $(this).attr('disabled','disabled');
                });
                $('.album-img').each(function() {
                    //console.log("a");
                     $(this).addClass('disableClick');
                });
            }
        var l = "currentPage"+id;
        var linkIdInt = link_id.match(/\d+$/)[0]; // getting only the number of id
        $('.slideshow-link').attr('id',l); //refresh current page to slideshow link
        if($(clicked_link).hasClass("hidden")){
            //console.log("has class hidden2");
            $.fancybox({
             beforeShow: function () {
             //console.log("fancybox2");
            this.title += '<div class="btn-group btn-group-justified">';
            var $links = $();
            //links.$('#a').css('visibility', 'hidden');
            $links.find('a').css('visibility','hidden');
             this.title += ' <div class="btn-group">';
             if ( typeof prev_id !== 'undefined'){
                    this.title += '<button type="button" id="prev-slide" class="btn  glyphicon glyphicon-chevron-left btn-primary" style="float:left"onclick="SlideShow('+prev_id+')">Prev page</button>';
                }  
            this.title += '</div>';
            this.title += ' <div class="btn-group">';    
            if ( typeof next_id !== 'undefined'){
                this.title += '<button type="button" id="next-slide" class="btn  glyphicon glyphicon-chevron-right btn-primary" style="float:right" onclick="SlideShow('+next_id+')">Next page</button>';
            }   
            this.title += '</div>';
            this.title += '</div>';
            },
            'content': data,
            closeBtn: true, 
            arrows: true,
            'transitionIn': 'none', 
            'transitionOut': 'none',
            'titlePosition': 'over',
            'autoScale' : true,
            openEffect : 'elastic',
            closeEffect : 'elasatic',
            helpers: {
            title: {
                type: 'inside'
            }, 
            buttons: {} 
        },
        closeBtn: true,  
        arrows: true,
            autoSize: true, // shouldn't be true ?
            fitToView: true,
           'transitionIn': 'none', 
        'transitionOut': 'none',
        'titlePosition': 'over',
        'titleFormat': function (title, currentArray, currentIndex, currentOpts) {
            return '<span id="fancybox-title-over">Image ' + (currentIndex + 1) + ' / ' + currentArray.length + (title.length ? ' &nbsp; ' + title : '') + '</span>';
            } 
        });
        }
      }
    });
    return false;
}
