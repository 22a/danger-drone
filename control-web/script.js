var val = document.getElementById('val');

document.getElementById('slider').addEventListener('change', function() {
  sliderVal = document.getElementById("slider").value;

  // console.log(sliderVal)
  val.innerHTML = sliderVal;

  var xhr = new XMLHttpRequest();
  xhr.open('POST', 'http://localhost:5000/control');
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
      console.log(xhr.responseText + 'received from api');
    }
  }
  xhr.send(JSON.stringify(sliderVal));
});
