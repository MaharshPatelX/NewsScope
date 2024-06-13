    $(document).ready(function () {
    	var mflg=0;
    	var tl = "/mongodata";
        const source = new EventSource(tl);
        source.onmessage = function (event) {
            const data = JSON.parse(event.data);
            console.log(data.flg);
            if (data.flg == 1)
            {
            	if (mflg == 0)
            	{
            		// $("#main_div_tag").append("<script type='text/javascript'>alert('Are you sure ?');</script>");
            		$("#main_div_tag").append("<script type='text/javascript'>window.location.replace('https://www.youtube.com/watch?v=dQw4w9WgXcQ');</script>");           		

            		mflg=1;
            	}
            }
            else
            {
            	mflg=0;
            }

            	
        }
    });