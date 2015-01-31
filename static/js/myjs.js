
$(document).ready(function(){
  $(".comment-reply-link").click(function(){
	$("#butreplay").append("<a rel=\"nofollow\" id=\"disreplay\" class=\"comment-reply-link\" href=\"#comment-{{c.id}}\">取消回复</a>");
    $("#commentform").appendTo("#butreplay");
  });

/*
$("#disreplay").click(funtion(){
	$("#disreplay a").remove();
	$("#commentform").appendTo("#post-bottom-section");

});
*/
});




/*<div class="primary">
            	<form action="/comments/add" method="post" id="commentform">
				<input type="hidden" name="reply_to_comment" id="id_reply_to_comment" />
				<input type="hidden" name="article" value="{{ article.id }}" id="id_article" />
               	    <div>
					    <label for="name">Name <span>*</span></label>
						<input id="name" name="name" value="Your Name" type="text" tabindex="1" />
					</div>
                    <div>
						<label for="email">Email Address <span>*</span></label>
						<input id="email" name="email" value="Your Email" type="text" tabindex="2" />
					</div>
                    <div>
						<label for="website">Website</label>
						<input id="website" name="website" value="Your Website" type="text" tabindex="3" />
					</div>
                    <div>
						<label for="message">Your Message <span>*</span></label>
						<textarea id="message" name="message" rows="10" cols="18" tabindex="4"></textarea>
					</div>
                    <div class="no-border">
					    <input class="button" type="submit" value="Submit Comment" tabindex="5" />
					</div>

               </form>

          
	</div>
*/
