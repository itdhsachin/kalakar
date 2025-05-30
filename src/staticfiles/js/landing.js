
window.onload = function() {
  var windowOn = window;

  // Preloader
  setTimeout(function() {
      var preloader = document.getElementById("back__preloader");
      if (preloader) {
          preloader.style.transition = "opacity 0.4s";
          preloader.style.opacity = "0";
          setTimeout(function() {
              preloader.style.display = "none";
          }, 400);
      }
  }, 1000);
};




//  Sticky header
function TopOffset(el) {
  let rect = el.getBoundingClientRect(),
    scrollTop = window.pageYOffset || document.documentElement.scrollTop;
  return { top: rect.top + scrollTop };
}
function ScrollSticky(){
  const headerStickyWrapper = document.querySelector('header');
  const headerStickyTarget = document.querySelector('.header__sticky');

  if(headerStickyTarget){
    window.addEventListener('scroll', function(){
      let StickyTargetElement = TopOffset(headerStickyWrapper);
      let TargetElementTopOffset = StickyTargetElement.top;

      if(window.scrollY > TargetElementTopOffset ){
        headerStickyTarget.classList.add('sticky');
      }else{
        headerStickyTarget.classList.remove('sticky');
      }
    })
  }
}
ScrollSticky();




// Scroll up activation
const scrollTop = document.getElementById("scroll-top");
scrollTop.addEventListener("click", function () {
  window.scroll({ top: 0, left: 0, behavior: "smooth" });
});

window.addEventListener("scroll", function () {
  if (window.scrollY > 300) {
    scrollTop.classList.add("active");
  } else {
    scrollTop.classList.remove("active");
  }
});





// ===========tab area==================
window.addEventListener("load", function() {
	// store tabs variable
	var myTabs = document.querySelectorAll("ul.nav-tabs > li");
  function myTabClicks(tabClickEvent) {
		for (var i = 0; i < myTabs.length; i++) {
			myTabs[i].classList.remove("active");
		}
		var clickedTab = tabClickEvent.currentTarget;
		clickedTab.classList.add("active");
		tabClickEvent.preventDefault();
		var myContentPanes = document.querySelectorAll(".tab-pane");
		for (i = 0; i < myContentPanes.length; i++) {
			myContentPanes[i].classList.remove("active");
		}
		var anchorReference = tabClickEvent.target;
		var activePaneId = anchorReference.getAttribute("href");
		var activePane = document.querySelector(activePaneId);
		activePane.classList.add("active");
	}
	for (i = 0; i < myTabs.length; i++) {
		myTabs[i].addEventListener("click", myTabClicks)
	}
});




// ============Filter area=============
filterSelection("all")
function filterSelection(c) {
  var x, i;
  x = document.getElementsByClassName("filterDiv");
  if (c == "all") c = "";
  // Add the "show" class (display:block) to the filtered elements, and remove the "show" class from the elements that are not selected
  for (i = 0; i < x.length; i++) {
    w3RemoveClass(x[i], "show");
    if (x[i].className.indexOf(c) > -1) w3AddClass(x[i], "show");
  }
}

// Show filtered elements
function w3AddClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    if (arr1.indexOf(arr2[i]) == -1) {
      element.className += " " + arr2[i];
    }
  }
}

// Hide elements that are not selected
function w3RemoveClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    while (arr1.indexOf(arr2[i]) > -1) {
      arr1.splice(arr1.indexOf(arr2[i]), 1);
    }
  }
  element.className = arr1.join(" ");
}

// Add active class to the current control button (highlight it)
var btnContainer = document.getElementById("myBtnContainer");
var btns = btnContainer.getElementsByClassName("btn");
for (var i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("active");
    current[0].className = current[0].className.replace(" active", "");
    this.className += " active";
  });
}






//==========accordion===========
	//this is the button
	var acc = document.getElementsByClassName("course-accordion");
	var i;

	for (i = 0; i < acc.length; i++) {
		//when one of the buttons are clicked run this function
	  acc[i].onclick = function() {
		//variables
		var panel = this.nextElementSibling;
		var coursePanel = document.getElementsByClassName("course-panel");
		var courseAccordion = document.getElementsByClassName("course-accordion");
		var courseAccordionActive = document.getElementsByClassName("course-accordion active");

		/*if pannel is already open - minimize*/
		if (panel.style.maxHeight){
			//minifies current pannel if already open
			panel.style.maxHeight = null;
			//removes the 'active' class as toggle didnt work on browsers minus chrome
			this.classList.remove("active");
		} else { //pannel isnt open...
			//goes through the buttons and removes the 'active' css (+ and -)
			for (var ii = 0; ii < courseAccordionActive.length; ii++) {
				courseAccordionActive[ii].classList.remove("active");
			}
			//Goes through and removes 'activ' from the css, also minifies any 'panels' that might be open
			for (var iii = 0; iii < coursePanel.length; iii++) {
			  this.classList.remove("active");
			  coursePanel[iii].style.maxHeight = null;
			}
		  //opens the specified pannel
		  panel.style.maxHeight = panel.scrollHeight + "px";
		  //adds the 'active' addition to the css.
		  this.classList.add("active");
		} 
	  }//closing to the acc onclick function
	}//closing to the for loop.







    class TypeWriter {
        constructor(txtElement, words, wait = 3000) {
          this.txtElement = txtElement;
          this.words = words;
          this.txt = '';
          this.wordIndex = 0;
          this.wait = parseInt(wait, 8);
          this.type();
          this.isDeleting = false;
        }

        type() {
          // Current index of word
          const current = this.wordIndex % this.words.length;
          // Get full text of current word
          const fullTxt = this.words[current];

          // Check if deleting
          if(this.isDeleting) {
            // Remove char
            this.txt = fullTxt.substring(0, this.txt.length - 1);
          } else {
            // Add char
            this.txt = fullTxt.substring(0, this.txt.length + 1);
          }

          // Insert txt into element
          this.txtElement.innerHTML = `<span class="txt">${this.txt}</span>`;

          // change color for data-text
          this.txtElement.innerHTML = `<span class="txt">${this.txt}</span>`;

          // Initial Type Speed
          let typeSpeed = 100;

          if(this.isDeleting) {
            typeSpeed /= 2;
          }

          // If word is complete
          if(!this.isDeleting && this.txt === fullTxt) {
            // Make pause at end
            typeSpeed = this.wait;
            // Set delete to true
            this.isDeleting = true;
          } else if(this.isDeleting && this.txt === '') {
            this.isDeleting = false;
            // Move to next word
            this.wordIndex++;
            // Pause before start typing
            typeSpeed = 300;
          }

          setTimeout(() => this.type(), typeSpeed);
        }
      }

    // Init On DOM Load
    document.addEventListener('DOMContentLoaded', init);

    // Init App
    function init() {
      const txtElement = document.querySelector('.txt-type');
      const words = JSON.parse(txtElement.getAttribute('data-words'));
      const wait = txtElement.getAttribute('data-wait');
      // Init TypeWriter
      new TypeWriter(txtElement, words, wait);
    }






var swiper = new Swiper(".showcase__slider__active", {
    effect: 'cards',
    grabCursor: true,
    clickable: true,
    loop: true,

    pagination: {
      el: ".swiper-pagination",
      clickable: true,
      type: "fraction",
    },
    grabCursor: true,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
        clickable: true,
    },
    slidesPerView: 1,
  });




// Dark to light mode js
const lightToDarkButton = document.getElementById("light--to-dark-button");
lightToDarkButton?.addEventListener("click", function () {
    if (localStorage.getItem("theme-color")) {
      if (localStorage.getItem("theme-color") === "light") {
        document.documentElement.classList.add("is_dark");
        localStorage.setItem("theme-color", "dark");
        lightToDarkButton?.classList.add("dark--mode");
      } else {
        document.documentElement.classList.remove("is_dark");
        localStorage.setItem("theme-color", "light");
        lightToDarkButton?.classList?.remove("dark--mode");
      }
    } else {
      if (document.documentElement.classList.contains("is_dark")) {
        document.documentElement.classList.remove("is_dark");
        lightToDarkButton?.classList?.remove("dark--mode");
        localStorage.setItem("theme-color", "light");
      } else {
        document.documentElement.classList.add("is_dark");
        localStorage.setItem("theme-color", "dark");
        lightToDarkButton?.classList.add("dark--mode");
      }
    }
});


