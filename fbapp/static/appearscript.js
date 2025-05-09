// https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_toggle_hide_show
// https://www.reddit.com/r/learnjavascript/comments/sh8zsi/why_do_my_buttons_have_to_be_clicked_twice_to_run/
document.getElementById('tankButton').addEventListener('click', async function() {
    var x = document.getElementById("appearDiv");
    if (x.style.display === '') {
        x.style.display = "none";
    } if (x.style.display === 'none'){
        x.style.display = 'block';
    } else {
        x.style.display = "none";
    }
});

//https://stackoverflow.com/questions/76047301/working-with-csrf-token-in-javascript-via-fetch-api
//https://codecourse.com/articles/sending-a-csrf-token-when-making-fetch-requests-with-laravel
//https://stackoverflow.com/questions/65485435/how-can-i-send-a-csrf-token-in-a-form
document.getElementById('askButton').addEventListener('click', async function() {
    const question = document.getElementById('question').value;
    
    try {
        const response = await fetch('/tankbar/', {
            method: 'POST',
            headers: {
                'Content-Type':'application/json',
	    },
	    body: JSON.stringify({ question: question })
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('answer').innerText = data.answer;
        } else {
            const errorData = await response.json();
            console.error('Error:', errorData.error_message); 
        }
    } catch (error) {
        console.error('Request failed', error);
    }
});
