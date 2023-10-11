def getWebPage():
  html = """
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<head meta="" name="viewport" content="width=device-width,height=device-height,initial-scale=1,maximum-scale=1,minimum-scale=1,user-scalable=no">
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta name="viewport" content="width=device-width,height=device-height,initial-scale=1,maximum-scale=1,minimum-scale=1,user-scalable=no">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
<!DOCTYPE html>
<html>
<head>
  <title>Configuration Form</title>
  <script>
    function submitForm() {
      var form = document.getElementById("configForm");
      var formData = new FormData(form);
      
      // Convert form data to JSON
      var jsonData = {};
      for (var pair of formData.entries()) {
        jsonData[pair[0]] = pair[1];
      }
      
      // Display JSON data (for demonstration purposes)
      var jsonOutput = document.getElementById("jsonOutput");
      jsonOutput.textContent = JSON.stringify(jsonData, null, 2);
      
      // Send data back to server
      return jsonData
      
      // You can perform additional actions with the JSON data, such as sending it to a server or using it in your application
    }
  </script>
</head>
<body>
  <h1>Configuration Form</h1>
  <form id="configForm" method="GET" action="/submit">
    <label for="MqttBroker">MqttBroker:</label>
    <input type="text" name="MqttBroker"><br><br>
    
    <label for="MqttPort">MqttPort:</label>
    <input type="text" name="MqttPort"><br><br>
    
    <label for="MqttPublishQos">MqttPublishQos:</label>
    <input type="text" name="MqttPublishQos"><br><br>
    
    <label for="MqttClientID">MqttClientID:</label>
    <input type="text" name="MqttClientID"><br><br>
    
    <label for="MqttPublishTopic">MqttPublishTopic:</label>
    <input type="text" name="MqttPublishTopic"><br><br>
    
    <label for="MqttUSER">MqttUser:</label>
    <input type="text" name="MqttUser"><br><br>
    
    <label for="MqttPASSWORD">MqttPassword:</label>
    <input type="text" name="MqttPassword"><br><br>
    
    <label for="MqttPublishTime">MqttPublishTime:</label>
    <input type="text" name="MqttPublishTime"><br><br>        
    
    <label for="KeepAlive">KeepAlive:</label>
    <input type="text" name="KeepAlive"><br><br>
    
    <label for="Wifi-Name">Wifi-Name:</label>
    <input type="text" name="Wifi-Name"><br><br>
    
    <label for="Wifi-Password">Wifi-Password:</label>
    <input type="text" name="Wifi-Password"><br><br>
    
    <input type="submit" value="Submit" onclick="submitForm()>
  </form>
  
  <h2>JSON Output:</h2>
  <pre id="jsonOutput"></pre>
</body>
</html>
"""
  return html