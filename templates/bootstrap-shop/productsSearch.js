/**
 * Created by abdullahfadel on 4/11/2017.
 */
function productsDetails() {

    appendToInnerHtml1=[];


    head4='<div class="tab-pane  active" id="blockView">';
    head5='<ul class="thumbnails">';



for (i = 0; i<test.length; i += 1) {
    appendToInnerHtml1[i]='<li class="span3">'+'<div class="thumbnail">'+'<img src="http://127.0.0.1:8000/'+itemImages[i][1]+'" alt=""/>'+'</div>'+
            '<div class="caption">'+'<h5>'+itemInformations[i][1]+'</h5>'+'<h3 style="position: relative; left: 30%">'+itemInformations[i][2]+'</h3>'+
            ' <h4 style="text-align:center"><a class="btn" href="#">'+'View Details'+'<i></i></a></h4>'+'</div>'+'</div>'+'</li>';

}
head6='</ul>';
    head7='<hr class="soft"/>';
    head8='</div>';


    document.getElementById('viewAll').innerHTML =head4+head5+appendToInnerHtml1+head6+head7+head8+head8;}















