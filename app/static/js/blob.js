var blobCount = 10;
function randy(min, max) {
	return Math.floor(Math.random() * (1 + max - min) + min);
}

var time = 2,
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
  init.rot = randy(-25,25);
  init.rotX = randy(-25,25);
  init.rotY = randy(-25,25);
  init.rotZ = randy(-25,25);
  init.left = randy(-1,3) + "%";
  init.top = randy(-1,3) + "%";
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
    left: randy(-1,3) + "%",
    ease: Sine.easeInOut
  }, 0);
}
for (var i = 0; i < blobs.length; i++) {
  tl.to(blobs[i], time, {
    top: randy(-1,3) + "%",
    ease: Sine.easeInOut
  }, 0);
}
for (var i = 0; i < blobs.length; i++) {
  tl.to(blobs[i], time*2, {
    top: randy(-1,3) + "%",
    ease: Sine.easeInOut
  }, time);
}
for (var i = 0; i < blobs.length; i++) {
  tl.to(blobs[i], time*2, {
    left: randy(-1,3) + "%",
    ease: Sine.easeInOut
  }, time*2);
}
for (var i = 0; i < blobs.length; i++) {
  tl.to(blobs[i], time*2, {
    top: randy(-1,3) + "%",
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