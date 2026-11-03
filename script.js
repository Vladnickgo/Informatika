
 function equationSolution(){
let coefA = document.getElementById('val_a').value;
let coefB = document.getElementById('val_b').value;
let coefC = document.getElementById('val_c').value;
let message="Розв'язання";
console.log(coefA);
if (coefA!=""){
coefA=parseInt(coefA);
coefB=parseInt(coefB);
coefC=parseInt(coefC);
console.log(coefA);
let diskr=coefB*coefB-4*coefA*coefC;
console.log(diskr);
message+="<p>Обчислимо дискримінант</p>";
message+="<p><i><b>D = b<sup>2</sup> - 4ac = ";
message+="("+coefB+")<sup>2</sup> - 4*"+coefA+"*"+coefC
message+=" = "+diskr+"</b></i></p>";
if(diskr>0){
    let x1=(-coefB-Math.sqrt(diskr))/(2*coefA);
    let x2=(-coefB+Math.sqrt(diskr))/(2*coefA);
    message+="<p>Обчислимо корені рівняння:</p>";
    message+="<p><i><b>x<sub>1</sub> = ( "+-coefB;
    message+=" - sqrt("+diskr+"))/(2*"+coefA+") = "+x1;
    message+="<p><i><b>x<sub>2</sub> = ( "+-coefB;
    message+=" + sqrt("+diskr+"))/(2*"+coefA+") = "+x2;
}
else{
    if(diskr==0){
        let x=-coefB/(2*coefA);
        message+="<p>Обчислимо корінь рівняння:</p>";
        message+="<p><i><b>x = ( -"+coefB+"))/(2*"+coefA+") = "+x;
}
    else{
        message+="<p>Коренів немає</p>";
    }
}
}
else
{
    message="<p>Коефіцієнт <i><b>a</b></i>"; 
    message+=" повинен бути більше НУЛЯ!!!<p>";   
}
console.log(message);
document.getElementById('out').innerHTML=message;
}






