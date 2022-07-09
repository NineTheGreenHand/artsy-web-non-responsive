// This is the JavaScript file for the Artsy Project:

// Set div to visible:
function showDiv(divID) {
   if ($(divID).hasClass("hideit")) {
      $(divID).removeClass("hideit");
   }
}

// Set div to hidden:
function hideDiv(divID) {
   if (!$(divID).hasClass("hideit")) {
      $(divID).addClass("hideit");
   }
}

// Add the horizontal bar of content with artist picture and name.
// If this bar already exist, replace the original content and
// fill with the new content:
function addArtist(result) {
   var arrObject = jQuery.parseJSON(result);
   var arrLen = arrObject.artists.length;

   // First, we check if there is a artist table created before:
   if ($("form").hasClass("artist")) {
      $(".artist").remove();
   }

   // After that is done, we create the artist table: 
   if (arrLen == 0) {
      hideDiv("#artist-bar");
      hideDiv("#first-loading");
      hideDiv("#second-loading");
      showDiv("#no-result-container");
   } else {
      hideDiv("#no-result-container");
      for (let i = 0; i < arrLen; ++i) {
         var artist_id = arrObject.artists[i].id;
         var artist_name = arrObject.artists[i].name;
         var artist_picURL = arrObject.artists[i].picURL;

         if (artist_picURL == "/assets/shared/missing_image.png") {
            artist_picURL = "/static/images/artsy_logo.svg";
         }

         var htmlText = "<form class=\"artist\" id=" + artist_id + " onsubmit=\"return false\">" +
         "<img id=\"artist-pic\" src=" + artist_picURL + ">" +
         "<p>" + artist_name + "</p></form>";

         $("#artist-bar").append(htmlText); 
      }
      hideDiv("#first-loading");
      hideDiv("#second-loading");
      showDiv("#artist-bar");   
   }
}

// Add the biography based on information received from the backend.
// If there is a biography of another user already exist, replace 
// the original biography and fill with the new one:
function addBio(result) {
   var arrObject = jQuery.parseJSON(result);
   var name = arrObject.name;
   var birthday = arrObject.birthday;
   var deathday = arrObject.deathday;
   var nationality = arrObject.nationality;
   var bio = arrObject.bio;

   // First, we check if there is a artist bio created before:
   if ($("div").hasClass("artist-detail")) {
      $(".artist-detail").remove();
   }

   // Then generate the content:
   var firstPart = name + " (" + birthday + " - " + deathday + ")";
   var htmlText = "<div class=\"artist-detail\"><p id=\"bio-firstPart\">" + 
   firstPart + "</p><br><p id=\"bio-nationality\">" + nationality + 
   "</p><br><p id=\"bio-bio\">" + bio + "</p></div>";

   $("#artist-biography-container").append(htmlText);
   hideDiv("#second-loading");
   showDiv("#artist-biography-container");
}