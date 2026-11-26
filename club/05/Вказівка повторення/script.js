function calculate(){
clr();
var y;
for(var i=-5;i<6;i++){
if (i<0){
y=-i;
}
else{
	y=i
}
document.getElementById('out').innerHTML+="Для x="+i+" значення Y="+y+"<br>";

}
}

function clr(){
document.getElementById('out').innerHTML="";
}