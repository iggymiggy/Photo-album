var flickrSrc= "";
function addFlickrLink(src){
    //console.log("moi");
    //console.log("add flickr link: ", flickrSrc);
    document.getElementById('imgLink').value = flickrSrc;
    $.fancybox.close();
}

//function for Flickr serarch
function searchPics(yourKeywords) {
    //JSON call for images
    $.getJSON("http://api.flickr.com/services/feeds/photos_public.gne?jsoncallback=?",
    {
        lang    : 'en-us',
        tags    : yourKeywords,
        tagmode : 'all',
        limit   : '20',
        format  : 'json'
    },
    
    function(data){
        var imgInsert = "";
        var items = [];
        var counter = 0;
  // Load max 20 images from Flickr and show images
    $.each(data.items, function(i,item){
        if (i == 20) return false;
        var imgThumb = item.media.m.split('m.jpg')[0] + 'm.jpg'; //size of the image small max 240px
        var imgLarge = item.media.m.split('m.jpg')[0] + 'b.jpg'; //large size of the image for fancybox
        imgInsert += '<div class="avatar">';
        imgInsert += '<a href="' + imgLarge + '" rel="flickr_group" class="big_img" title="' + item.title + '">';
        imgInsert += '<img title="' + item.title + '" src="' + imgThumb + '" alt="' + item.title + '" />';
        imgInsert += '</a></div>';
        counter++;
    });

    //NO search results
    if (counter == 0){
        document.getElementById("addImageModalError").innerHTML="No search results";
        document.getElementById("addImageModalError").setAttribute("style","display:block;");
    }else{ //if results, hide no search results
        document.getElementById("addImageModalError").innerHTML="";
        document.getElementById("addImageModalError").setAttribute("style","display:none;");
    }
    //show images
    var cachedItems = $(imgInsert).data('cached', imgInsert);
    $('#flickrContent').append(imgInsert).addClass(yourKeywords).data('cached', data.items);

   //open the images bigger using fancybox
    $("a[rel=flickr_group]").fancybox({
         beforeShow: function () {
            $(this).css('z-value', '8040');
            // New line
            this.title += '<br />';
            // Add button for adding image to page
            flickrSrc = this.href;
            this.title += '<button type="button" id="copyFlickrLink" class="btn btn-primary " onclick="addFlickrLink()">Add this image</button>'; 
        },
        afterShow: function () {
            //nothing here at the moment
            $(this).css('z-value', '8040');
        },
        helpers: {
            title: {
                type: 'inside'
            }, 
            buttons: {} 
        },
        closeBtn: true, 
        arrows: true,
        'transitionIn': 'none', 
        'transitionOut': 'none',
        'titlePosition': 'over',
        'titleFormat': function (title, currentArray, currentIndex, currentOpts) {
            return '<span id="fancybox-title-over">Image ' + (currentIndex + 1) + ' / ' + currentArray.length + (title.length ? ' &nbsp; ' + title : '') + '</span>';
            }
        });                
    });
}
 
$( document ).ready(function() {
    //search images from flickr when button pressed
	$('.flickrSearch-btn').click(function(){
        //remove the old flickrContent and replace it with the new search
        if ( $('#flickrContent').length > 0 ) {
            $('#flickrContent').empty();
        }
        //set pictures
        searchPics(document.getElementById('flickrSearch').value );
        //document.getElementById('flickrImages').setAttribute("style","display:block; float:left;");
        return false;
  });
  // button for resetting image link area to delete image
  $('.reset-link-btn').click(function(){
        document.getElementById("link_form").reset();
       
  });
 
});
