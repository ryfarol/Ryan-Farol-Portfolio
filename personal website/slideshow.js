var slidePos = 1; // initialize index at the first slide
var auto = null; // auto variable will be used to keep track of the slides automatically moving fowrward 
showSlides(slidePos);

// Move forward or back
function plusSlides(n) {
  clearTimeout(auto); // clearTimeout will be called when the next/prev button is clicked 
  showSlides(slidePos += n);
}

// current image indicator 
function currentSlide(n) {
  clearTimeout(auto); // clearTimeout called when next/prev button is clicked
  showSlides(slidePos = n);
}

//showSlides function outputs the slides either automatically or by the next/prev buttons
function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("Slides");
  var indicator = document.getElementsByClassName("dot");
  if (n==null){n = ++slidePos} // keeps moving the slides forward until plusslides function is called
  if (n > slides.length) {slidePos = 1}
  if (n < 1) {slidePos = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  for (i = 0; i < indicator.length; i++) {
      indicator[i].className = indicator[i].className.replace(" active", "");
  }
  slides[slidePos-1].style.display = "block";
  indicator[slidePos-1].className += " active";
  auto = setTimeout(showSlides, 5000); // setTimeout is placed to keep the slides autmomatically moving forward every 5 seconds
}
