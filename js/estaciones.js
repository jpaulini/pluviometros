var intaJSONObject = {};
var client = new XMLHttpRequest();

client.open("GET", "srv1", false);
try {
	// Sometimes it raises XMLHTTPRequestException 101
	client.send();
	intaJSONObject = JSON.parse( client.responseText ) ;

} catch (e) { 
	intaJSONObject = {} ;
	alert("No Data!")

}
finally {
	client.abort();
}




