/**
 * New cookiebar functionality, as a Javascript module.
 *
 * About modules: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules
 *
 */
const DEFAULTS = {
  // TODO: also accept element rather than selector?
  templateSelector: '#cookie-consent__cookie-bar',
  cookieGroupsSelector: '#cookie-consent__cookie-groups',
  acceptSelector: '.cookie-consent__accept',
  declineSelector: '.cookie-consent__decline',
  /**
   * Either a string (selector), DOMNode or null.
   *
   * If null, the bar is appended to the body. If provided, the node is used or looked
   * up.
   */
  insertBefore: null,
  onShow: null, // callback when the cookie bar is being shown -> add class to body...
  onAccept: null, // callback when cookies are accepted
  onDecline: null, // callback when cookies are declined
};

export const loadCookieGroups = (selector) => {
  const node = document.querySelector(selector);
  if (!node) {
    throw new Error(`No cookie groups (script) tag found, using selector: '${selector}'`);
  }
  return JSON.parse(node.innerText);
};

const doInsertBefore = (beforeNode, newNode) => {
  const parent = beforeNode.parentNode;
  parent.insertBefore(newNode, beforeNode);
}

/**
 * Register the accept/decline event handlers.
 *
 * Note that we can't just set the decline or accept cookie purely client-side, as the
 * cookie possibly has the httpOnly flag set.
 *
 * @param  {HTMLEelement} cookieBarNode The DOM node containing the cookiebar markup.
 * @param  {Object} options       The options as passed to showCookieBar, containing the selectors
 * @return {Void}
 */
const registerEvents = (cookieBarNode, options) => {
  cookieBarNode
    .querySelector(options.acceptSelector)
    .addEventListener('click', event => {
      event.preventDefault();
      console.log('accept clicked');
      options.onAccept?.(event);
      // TODO: discover scripts to toggle to text/javascript or module type
      // TODO: make backend call to accept cookies
    });

  cookieBarNode
    .querySelector(options.declineSelector)
    .addEventListener('click', event => {
      event.preventDefault();
      console.log('decline clicked');
      options.onDecline?.(event);
      // TODO: provide beforeDeclined hook?
      // TODO: discover scripts to disable
      // TODO: make backend call to decline cookies
    });
};

export const showCookieBar = (options={}) => {
  // merge defaults and provided options
  options = {...DEFAULTS, ...options};
  const {
    cookieGroupsSelector,
    templateSelector,
    insertBefore,
    onShow,
  } = options;
  const cookieGroups = loadCookieGroups(cookieGroupsSelector);

  // no cookie groups -> abort
  if (!cookieGroups.length) return;

  const templateNode = document.querySelector(templateSelector);

  // insert before a given node, if specified, or append to the body as default behaviour
  const doInsert = insertBefore === null
    ? (cookieBarNode) => document.querySelector('body').appendChild(cookieBarNode)
    : typeof insertBefore === 'string'
      ? (cookieBarNode) => doInsertBefore(document.querySelector(insertBefore), cookieBarNode)
      : (cookieBarNode) => doInsertBefore(insertBefore, cookieBarNode)
  ;
  // grab the contents from the template node and add them to the DOM, optionally
  // calling the onShow callback
  const cookieBarNode = templateNode.content.firstElementChild.cloneNode(true);
  registerEvents(cookieBarNode, options);
  onShow?.();
  doInsert(cookieBarNode);
};
