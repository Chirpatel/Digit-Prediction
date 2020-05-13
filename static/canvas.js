window.addEventListener('load',()=>{
    const canvas = document.querySelector("#canvas");
    const ctx = canvas.getContext('2d');

    canvas.height = 280;
    canvas.width  = 280;
		//ctx.fillStyle = 'green';
    //ctx.fillRect(0, 0, canvas.width, canvas.height);
    let painting =false;
    function startPosition(e){
        painting=true;
        draw(e);
    }
    function finishedPosition(){
        painting = false;
        ctx.beginPath();
    }
    function draw(e){
        if(!painting) return;
        ctx.lineWidth=20;
        ctx.lineCap = "round";
        ctx.lineTo(e.clientX,e.clientY);
        ctx.stroke();
        /*ctx.beginPath();
        ctx.moveTo(e.clientX,e.clientY);*/
    }
    canvas.addEventListener("mousedown",startPosition);
    canvas.addEventListener("mouseup",finishedPosition);
    canvas.addEventListener("mousemove",draw);
    document.getElementById("Submit").addEventListener("click",predict);
    function predict(){
        document.getElementById("downloader").download = "image.png";
        document.getElementById("downloader").href = document.getElementById("canvas").toDataURL()
						let message = {
								image: document.getElementById("canvas").toDataURL().replace("data:image/png;base64,","")
						}
						console.log(message);

						$.post("https://number-prediction.chir0313.repl.co/",JSON.stringify(message), function(response){
								$("#d-prediction").text(response.prediction);
								console.log(response);
						});

    }

})
