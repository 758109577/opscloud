$(".server").click(function(e){
	e.preventDefault();
	var server_name = $(this).text();
	$.ajax({
		url: '/server/',
		type: 'get',
		data: {'server_name': server_name},
		success: function(data){
			//alert(data);
			//var list = eval('(' + data + ')');
			//alert(list.length);
			//for(var i = 0; i < list.length; i++){
			//	for(var j = 0; j < list[i].length; j++){
			//		alert(list[i][j]);
			//	}
			//}
			window.location.href="/server_app/?id="+data;
		}
	});
});

$(".server_add_btn").click(function(){
	$("table").hide();
	$("#server_form").removeAttr("style");
});

$("#cancel").click(function(){
	window.location.reload();
});
