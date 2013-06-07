(function ($) {
  $.showCookieBar = function (options) {
    var defaults = {
      content: '',
      cookie_groups: [],

      cookie_decline: null, // set cookie_consent decline on client immediately
      beforeDeclined: null
    };

    var opts = $.extend(defaults, options);
    var $content = $(opts.content);

    $('body').append($content).addClass('with-cookie-bar');

    $('.cc-cookie-accept', $content).click(function() {
      $.post($(this).attr('href'));
      // document.cookie = cookie_accept;
      $content.hide();
      $('body').removeClass('with-cookie-bar');
      $("script[type='x/cookie_consent']").each(function() {
        if (cookie_groups.indexOf($(this).attr('data-varname')) != -1) {
          var src = $(this).attr('src');
          if (src) {
            var script = document.createElement('script');
            script.src = src;
            document.getElementsByTagName("head")[0].appendChild(script);
          } else {
            $.globalEval(this.innerHTML);
          }
        }
      });
      return false;
    });

    $('.cc-cookie-decline', $content).click(function() {
      if ($.isFunction(opts.declined)) {
          opts.declined();
        }
      $.post($(this).attr('href'));
      if (opts.cookie_decline) {
        document.cookie = opts.cookie_decline;
      }
      $content.hide();
      $('body').removeClass('with-cookie-bar');
      return false;
    });

 };
})(jQuery);
