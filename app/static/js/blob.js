var blobCount = 10;
function randy(min, max) {
	return Math.floor(Math.random() * (1 + max - min) + min);
}

var time = 15,
    tl = new TimelineMax({repeat: -1,yoyo:false}),
    container = document.getElementById("container");
for (var i = 0; i < blobCount; i++) {
  var div = document.createElement("div");
  container.appendChild(div);
}
var blobs = container.children;
initSettings = [];
for (var i = 0; i < blobs.length; i++) {
  var init = {};
  init.rot = randy(-250,250);
  init.rotX = randy(-250,250);
  init.rotY = randy(-250,250);
  init.rotZ = randy(-250,250);
  init.left = randy(-4,13) + "%";
  init.top = randy(-4,13) + "%";
  initSettings.push(init);
  tl.set(blobs[i], {
    rotation: init.rot,
    rotationX: init.rotX,
    rotationY: init.rotY,
    rotationZ: init.rotZ,
    left: init.left,
    top: init.top,
  });
}
for (var i = 0; i < blobs.length; i++) {
  tl.to(blobs[i], time*3, {
    rotation: "+="+360,
    rotationX: "+="+360,
    rotationY: "+="+360,
    rotationZ: "+="+360,
    ease: Power0.easeNone
  }, 0);
}
for (var i = 0; i < blobs.length; i++) {
  tl.to(blobs[i], time*2, {
    left: randy(-4,13) + "%",
    ease: Sine.easeInOut
  }, 0);
}
for (var i = 0; i < blobs.length; i++) {
  tl.to(blobs[i], time, {
    top: randy(-4,13) + "%",
    ease: Sine.easeInOut
  }, 0);
}
for (var i = 0; i < blobs.length; i++) {
  tl.to(blobs[i], time*2, {
    top: randy(-4,13) + "%",
    ease: Sine.easeInOut
  }, time);
}
for (var i = 0; i < blobs.length; i++) {
  tl.to(blobs[i], time*2, {
    left: randy(-4,13) + "%",
    ease: Sine.easeInOut
  }, time*2);
}
for (var i = 0; i < blobs.length; i++) {
  tl.to(blobs[i], time*2, {
    top: randy(-4,13) + "%",
    ease: Sine.easeInOut
  }, time*3);
}
for (var i = 0; i < blobs.length; i++) {
  tl.to(blobs[i], time*2, {
    left: initSettings[i].left,
    ease: Sine.easeInOut
  }, time*4);
}
for (var i = 0; i < blobs.length; i++) {
  tl.to(blobs[i], time, {
    top: initSettings[i].top,
    ease: Sine.easeInOut
  }, time*5);
}