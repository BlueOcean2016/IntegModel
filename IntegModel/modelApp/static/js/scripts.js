//MobileMenu 
function mobileMenu() {
  var e = $("#js-nav-mobile-menu").unbind();
  $("#js-nav-menu").removeClass("show"), e.on("click", function (e) {
    e.preventDefault(), $("#js-nav-menu").slideToggle(function () {
      $("#js-nav-menu").is(":hidden") && $("#js-nav-menu").removeAttr("style")
    })
  })
}

//Language Selector
function toggleLanguage() {
  $("#language-selector").click(function () {
    $("#language-selector .submenu").toggleClass("displayMenu"),
    $("#language-selector > a").toggleClass("up-arrow")
  })
}

//Mobile Menu Button
function hamburgerIcon() {
  $(".toggle-container").click(function () {
    $(".toggle-switch").toggleClass("active"),
    $(".toggle-text").toggleClass("active"),
    $("#language-selector .submenu").removeClass("displayMenu"),
    $("#language-selector > a").removeClass("up-arrow")
  })
}

//Generic Toggle Buttons
function toggleButton() {
  $(".checkbox").click(function () {
    $(".checkbox").not(this).removeClass("active").siblings("input").prop("checked", !1),
    $(this).addClass("active").siblings("input").prop("checked", !0)
  })
}

//Map Switcher
function toggleMap() {
  $("#singapore").click(function () {
    $("#singapore").addClass("active"),
    $("#dalian, #tokyo, #shanghai").removeClass("active")
  }),
    $("#dalian").click(function () {
      $("#dalian").addClass("active"),
      $("#singapore, #tokyo, #shanghai").removeClass("active")
  }),
    $("#tokyo").click(function () {
      $("#tokyo").addClass("active"),
      $("#singapore, #dalian, #shanghai").removeClass("active")
  }),
    $("#shanghai").click(function () {
      $("#shanghai").addClass("active"),
      $("#singapore, #dalian, #tokyo").removeClass("active")
  })
}

//Tooltip
function tooltip() {
  $(function () {
    var e = $("[rel~=tooltip]"),
      t = !1,
      o = !1,
      i = !1;
    overflow = !1, e.bind("mouseenter", function () {
      if (t = $(this), tip = t.attr("title"), o = $('<div class="tooltip"></div>'), i = $('<div class="question-mark"></div>'), overflow = $('<div class="overflow"></div>'), !tip || "" == tip) return !1;
      t.removeAttr("title"), o.css("opacity", 0).appendTo("body"), i.prependTo(o), overflow.html(tip).appendTo(o);
      var e = function () {
        $(window).width() < 1.5 * o.outerWidth() ? o.css("max-width", $(window).width() / 2) : o.css("max-width", 340);
        var e = t.offset().left + t.outerWidth() / 2 - o.outerWidth() / 2,
          i = t.offset().top - o.outerHeight() - 20;
        if (0 > e ? (e = t.offset().left + t.outerWidth() / 2 - 20, o.addClass("left")) : o.removeClass("left"), e + o.outerWidth() > $(window).width() ? (e = t.offset().left - o.outerWidth() + t.outerWidth() / 2 + 20, o.addClass("right")) : o.removeClass("right"), 0 > i) {
          var i = t.offset().top + t.outerHeight();
          o.addClass("top")
        } else o.removeClass("top");
        o.css({
          left: e,
          top: i
        }).animate({
          top: "+=10",
          opacity: 1
        }, 50)
      };
      e(), $(window).resize(e);
      var a = function () {
        o.animate({
          top: "-=10",
          opacity: 0
        }, 50, function () {
          $(this).remove()
        }), t.attr("title", tip)
      };
      t.bind("mouseleave", a), o.bind("click", a)
    })
  })
}

//Accordion
function accordion() {
  $(".accordion-button").bind("click", function (e) {
    $(".accordion-form").slideToggle(500).toggleClass("is-expanded"), e.preventDefault()
  }), $(".reset-accordion").bind("click", function (e) {
    $(".accordion-form").slideToggle(200).toggleClass("is-expanded"), e.preventDefault()
  })
}

//SmoothScroll
function smoothscroll() {
  $("a[href*=#]:not([href=#])").click(function () {
    if (location.pathname.replace(/^\//, "") == this.pathname.replace(/^\//, "") && location.hostname == this.hostname) {
      var e = $(this.hash);
      if (e = e.length ? e : $("[name=" + this.hash.slice(1) + "]"), e.length) return $("html,body").animate({
        scrollTop: e.offset().top
      }, 500), !1
    }
  })
}

//Run
$(document).ready(function () {
  mobileMenu(),
  toggleLanguage(),
  hamburgerIcon(), 
  toggleButton(), 
  toggleMap(),
  tooltip(),
  accordion(),
  smoothscroll()
});
