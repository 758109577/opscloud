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
			window.location.href="/server_app/?id="+data+'&server_name='+server_name;
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

/*
$("#delete_server").click(function(){
	$(".server_checkbox").change(function(){
		var checked = $(this).is(":checked");
		if (checked) {
			alert("1");
		} else {
			alert("0");
		}
	});
});
*/
$(".server_checkbox").change(function(){
	var checked = $(this).is(":checked");
	var parentNode = $(this).parent().parent().parent().parent();
	var node_ip_ele = parentNode.children("#ip");
	var node_name_ele = parentNode.children("#server_name");
	var	node_name = node_name_ele.text();
	var	node_ip = node_ip_ele.text();
	if (checked) {
		$(this).attr("checked", true);
		$("#delete_server").click(function(){
			$.ajax({
        		url: '/server_del/',
        		type: 'post',
        		data: {'node_ip': node_ip, 'node_name': node_name},
        		success: function(data){
					//window.location.reload();
					window.location.href="/index/";
				}
			});
		});
	}
	else {
		$(this).attr("checked", false);
	}
});

/*
$(".server_manager").click(function(e){
	e.preventDefault();
	var ele_text = $(this).text();
	if (ele_text=="编译管理"){
    	$(".clearfix").hide();
    	$("table").hide();
		//$(".clearfix").addClass('compilehide');
    	$("#compile_form").removeAttr("style");
	}
	//else {
	//	alert("查看server.js");
	//}
});
*/


$(".server_checkbox").click(function(){
	var is_check = $(this).prop('checked');
	app_name = $(this).parent().parent().parent().next().text();
	host_ip = $(this).parent().parent().parent().next().next().text();
	port = $(this).parent().parent().parent().next().next().next().text();
	if (is_check){
		$(".server_manager").click(function(e){
    		e.preventDefault();
    		var ele_text = $(this).text();
			if(ele_text=='发布服务'){
				$(".clearfix").hide();
				$("table").hide();
				$("#publish_form").removeAttr("style");
				/*
				$.ajax({
                url: '/server_publish/',
                type: 'post',
                data: {'app_name': app_name, 'host_ip': host_ip, 'port': port},
                success: function(data){
					return data;
					}	
				});
				*/
			}
			else if(ele_text=="启动服务"){
				alert("启动服务");
			}
			else if(ele_text=="编译管理"){
				$(".clearfix").hide();
		        $("table").hide();
				$("#compile_form").removeAttr("style");
			}
			else{
				alert("停止服务");
			}
		});
	}
	else{
		alert('no');
	}
});

$("#compile").click(function(){
	var project_name = $("#project_name").val();
	var git_url = $("#ssh_url option:selected").text();
	$.ajax({
    	url: '/git_url/',
        type: 'post',
        data: {'git_url': git_url, 'project_name': project_name},
        success: function(log_info){
			console.log(log_info);	
		}
	});
});
