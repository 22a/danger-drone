var val = document.getElementById('val');

document.getElementById('slider').addEventListener('change', function() {
  slider_val = document.getElementById('slider').value;
  post('http://192.168.43.224:5000/control', slider_val, function(res){
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
  post('http://192.168.43.224:5000/detect', {}, function(emotion_res){
    json = JSON.parse(emotion_res.replace(/'/g, '"'));
    console.log(json);
    val.innerHTML = emotion_string(json);
  });
}

var find_emotion = function(){
  var slider_container = document.getElementById('slider-container');
  var emotion_container = document.getElementById('emotion-container');
  slider_container.style.display = "none";
  emotion_container.style.display = "none";

  emotion_loop('happiness', function(){
    slider_container.style.display = "block";
    emotion_container.style.display = "block";
  });
}

var emotion_loop = function(target_emotion, callback){
  var interval = null;
  interval = setIntervalAndExecute(function() {
    random_direction = Math.ceil(Math.random() * 100);
    random_direction_str = '' + random_direction;
    post('http://192.168.43.224:5000/control', random_direction_str, function(control_res){
     setTimeout(function(){
        post('http://192.168.43.224:5000/detect', {}, function(emotion_res){
          emotions = JSON.parse(emotion_res.replace(/'/g, '"'))
          val.innerHTML = emotion_string(emotions);
          if (emotions[target_emotion] > 0){
            clearInterval(interval);
            callback();
          }
      });
      }, 500);
    });
  }, 3000);
}

var setIntervalAndExecute = function(fn, t) {
  fn();
  return(setInterval(fn, t));
}

var emotion_string = function(emotions){
  var str = '';
  var map = {
    'anger':'😠',
    'contempt':'🙄',
    'disgust':'🤢',
    'fear':'😱',
    'happiness':'😄',
    'neutral':'😐',
    'sadness':'😞',
    'surprise':'😯'
  }
  for (emotion in emotions){
    if (emotions[emotion] > 0){
      str = str + emotions[emotion] + ' ' + map[emotion] + '<br>';
    }
  }
  return str;
}
