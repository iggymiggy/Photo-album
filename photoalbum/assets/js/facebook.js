window.fbAsyncInit = function() {
  // Configuration options for the FB SDK
  FB.init({
    appId: '635924499799518',
    status: true,
    cookie: true,
    xfbml: true
  });

  // Javascript event for all authentication related changes
  FB.Event.subscribe('auth.authResponseChange', function(response){
    if (response.status === 'connected') { // User has logged into our app
      FB.logout();
    } else if (response.status === 'not_authorized') { // User has not logged into our app, but has logged into FB
      FB.login();
    } else { // User has not logged into both our app and FB
      FB.login();
    }
  });
};
