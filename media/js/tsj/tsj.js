var PythonR = PythonR || {};

PythonR.build_chart = function(response_json){
	if (response_json && response_json.csv){
		var dygraph = new Dygraph(
      document.getElementById("chart"),
      response_json.csv
    );
	}
};

$(function(){
	$.ajax({
		url : "/get_data/",
		type : "get",
		success : PythonR.build_chart,
		error : function(){
			alert("oh noes!");
		}
	});
});