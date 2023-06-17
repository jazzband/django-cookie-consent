function evalXCookieConsent(script) {
  var src = script.getAttribute("src")
  if (src) {
      var newScript = document.createElement('script');
      newScript.src = src;
      document.getElementsByTagName("head")[0].appendChild(newScript);
  } else {
      eval(script.innerHTML);
  }
  script.remove();
}

function lecacyShowCookieBar (options) {
  const defaults = {
    content: '',
    cookie_groups: [],

    cookie_decline: null, // set cookie_consent decline on client immediately
    beforeDeclined: null
  };

  const opts = Object.assign(defaults, options);
  
  const wrapper = document.createElement('div');
  wrapper.innerHTML= opts.content;
  const content = wrapper.firstChild;

  const body = document.querySelector('body');
  body.appendChild(content);
  body.classList.add('with-cookie-bar');

  document
  .querySelector(".cc-cookie-accept", content)
  .addEventListener('click', (e) => {
    e.preventDefault();
    fetch(e.target.getAttribute("href"), {method: "POST"})
    .then(() => {
      content.style.display = "none";
      body.classList.remove('with-cookie-bar');
      scripts = document.querySelectorAll("script[type='x/cookie_consent']");
      scripts.forEach( (script) => {
        if (cookie_groups.indexOf(script.getAttribute('data-varname')) != -1) {
          evalXCookieConsent(script);
        }
      });
    })  
  });

  document
  .querySelector(".cc-cookie-decline", content)
  .addEventListener('click', (e) => {
    e.preventDefault();
    if (typeof opts.beforeDeclined === "function") {
      opts.beforeDeclined();
    }
    fetch(e.target.getAttribute("href"), {method: "POST"})
    .then(() => {
      content.style.display = "none";
      body.classList.remove('with-cookie-bar');
      if (opts.cookie_decline) {
        document.cookie = opts.cookie_decline;
      }
    })  
  });
}

window.legacyShowCookieBar = window.showCookieBar = lecacyShowCookieBar;
