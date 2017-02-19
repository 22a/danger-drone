var val = document.getElementById('val');

document.getElementById('slider').addEventListener('change', function() {
  slider_val = document.getElementById('slider').value;
  val.innerHTML = slider_val;
  post('http://localhost:5000/control', slider_val, function(res){
    console.log(res);
  })
});

var post = function(endpoint, body, callback){
  var xhr = new XMLHttpRequest();
  xhr.open('POST', endpoint);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
      callback(xhr.responseText);
    }
  }
  xhr.send(JSON.stringify(body));
}

var detect = function(){
  post('http://localhost:5000/detect', {}, function(emotion_res){
    console.log(JSON.parse(emotion_res.replace(/'/g, '"')));
  });
}

var find_emotion = function(){
  var slider_container = document.getElementById('slider-container');
  var emotion_container = document.getElementById('emotion-container');
  slider_container.style.display = "none";
  emotion_container.style.display = "none";

  emotion_loop(function(){
    slider_container.style.display = "block";
    emotion_container.style.display = "block";
  });
}

var emotion_loop = function(callback){
  var interval = null;
  interval = setIntervalAndExecute(function() {
    random_direction = Math.ceil(Math.random() * 100);
    post('http://localhost:5000/control', random_direction, function(control_res){
      post('http://localhost:5000/detect', {}, function(emotion_res){
        emotions = JSON.parse(emotion_res.replace(/'/g, '"'))
        // console.log(emotions)
        if (emotions.happiness > 0){
          clearInterval(interval);
          callback();
        }
      });
    });
  }, 3000);
}

var setIntervalAndExecute = function(fn, t) {
  fn();
  return(setInterval(fn, t));
}
