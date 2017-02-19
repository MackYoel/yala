var $loadergif = $('#s-loader')
var $sessionBlock = $('#session-block')
var $sessionStart = $('#session-start')
var $fbLoginButton = $('#fb-login-button')
var $goHome = $('#go-home')

$goHome.click(function(){ window.location.href='/'})

function continueLike(fbData){
	return function(){
		$loadergif.show()
		fbData.csrfmiddlewaretoken = csrf_token;
		fbData.picture = fbData.picture.data.url;

	    $.post(window.location.href, fbData).done(function(data){
	        window.location.href = '/'
	    }).fail(function(err){
	    	alert('Oops! esto es embarazoso, comuníquese con el admin');
	    });
	}
}

function statusHandler(resp) {
    $loadergif.hide();$sessionBlock.show();
	var connectedOnFB = resp.status === 'connected'
	if (connectedOnFB) {
		if (!session_exists){
			getUserFromFacebook(function(fbData){
				$sessionStart.html(`Continuar como ${fbData.first_name}`)
				$sessionStart.show()
				$sessionStart.click(continueLike(fbData))
			})
		}
	} else {
		$fbLoginButton.show();
	}
}

function getUserFromFacebook(callback) {
	FB.api('/me', {fields: 'name,email,first_name,last_name,picture'},function(fb_data) {
		callback(fb_data);
    });
}

function onLoggedIn() {
	getUserFromFacebook(function(fbData){
		continueLike(fbData)()
	});
}
