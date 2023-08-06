/**
 * New cookiebar functionality, as a Javascript module.
 *
 * About modules: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules
 *
 * The code is organized here in a way to make the templates work with Django's page
 * cache. This means that anything user-specific (so different django session and even
 * cookie consent cookies) cannot be baked into the templates, as that breaks caches.
 *
 * The cookie bar operates on the following principles:
 *
 * - The developer using the library includes the desired template in their django
 *   templates, using the HTML <template> element. This contains the content for the
 *   cookie bar.
 * - The developer is responsible for loading some Javascript that loads this script.
 * - The main export of this script needs to be called (showCookieBar), with the
 *   appropriate options.
 * - The options include the backend URLs where the retrieve data, which selectors/DOM
 *   nodes to use for various functionality and the hooks to tap into the accept/decline
 *   life-cycle.
 * - When a user accepts or declines (all) cookies, the call to the backend is made via
 *   a fetch request, bypassing any page caches and preventing full-page reloads.
 */
const DEFAULTS = {
  statusUrl: undefined,
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
  csrfHeaderName: 'X-CSRFToken', // Django's default, can be overridden with settings.CSRF_HEADER_NAME
};

const DEFAULT_HEADERS = {'X-Cookie-Consent-Fetch': '1'};

let CONFIGURATION = DEFAULTS;
/**
 * Cookie accept status, including the accept/decline URLs, csrftoken... See
 * backend view CookieStatusView.
 */
let COOKIE_STATUS = null;

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
 * @return {Void}
 */
const registerEvents = (cookieBarNode) => {
  const {acceptSelector, onAccept, declineSelector, onDecline} = CONFIGURATION;

  cookieBarNode
    .querySelector(acceptSelector)
    .addEventListener('click', event => {
      event.preventDefault();
      onAccept?.(event, COOKIE_STATUS.cookieGroups);
      acceptCookiesBackend();
      cookieBarNode.parentNode.removeChild(cookieBarNode);
    });

  cookieBarNode
    .querySelector(declineSelector)
    .addEventListener('click', event => {
      event.preventDefault();
      onDecline?.(event, COOKIE_STATUS.cookieGroups);
      // TODO: provide beforeDeclined hook?
      declineCookiesBackend();
      cookieBarNode.parentNode.removeChild(cookieBarNode);
    });
};

const loadCookieStatus = async () => {
  const {statusUrl} = CONFIGURATION;
  if (!statusUrl) console.error('Missing status URL option, did you forget to pass the statusUrl option?');
  const response = await window.fetch(
    CONFIGURATION.statusUrl,
    {
      method: 'GET',
      credentials: 'same-origin',
      headers: DEFAULT_HEADERS
    }
  );
  // assign to module level variable, once the page is loaded these details should
  // not change.
  COOKIE_STATUS = await response.json();
};

const saveCookiesStatusBackend = async (urlProperty) => {
  const status = COOKIE_STATUS || {};
  const url = status[urlProperty];
  if (!url) {
    console.error(`Missing url for ${urlProperty} - was the cookie status not loaded properly?`);
    return;
  }
  await window.fetch(url, {
    method: 'POST',
    credentials: 'same-origin',
    headers: {
      ...DEFAULT_HEADERS,
      [CONFIGURATION.csrfHeaderName]: status.csrftoken
    }
  });
}

/**
 * Make the call to the backend to accept the cookies.
 */
const acceptCookiesBackend = async () => await saveCookiesStatusBackend('acceptUrl');
/**
 * Make the call to the backend to decline the cookies.
 */
const declineCookiesBackend = async () => await saveCookiesStatusBackend('declineUrl');

export const showCookieBar = async (options={}) => {
  // merge defaults and provided options
  CONFIGURATION = {...DEFAULTS, ...options};
  const {
    cookieGroupsSelector,
    templateSelector,
    insertBefore,
    onShow,
  } = CONFIGURATION;
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
  await loadCookieStatus();
  // there are no (more) cookie groups to accept, don't show the bar
  if (!COOKIE_STATUS.cookieGroups.length) return;

  // grab the contents from the template node and add them to the DOM, optionally
  // calling the onShow callback
  const cookieBarNode = templateNode.content.firstElementChild.cloneNode(true);
  registerEvents(cookieBarNode);
  onShow?.();
  doInsert(cookieBarNode);
};
