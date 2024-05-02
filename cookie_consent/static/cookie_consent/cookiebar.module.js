// src/cookiebar.ts
var DEFAULT_FETCH_HEADERS = {
  "X-Cookie-Consent-Fetch": "1"
};
var FetchClient = class {
  constructor(statusUrl, csrfHeaderName) {
    this.statusUrl = statusUrl;
    this.csrfHeaderName = csrfHeaderName;
    this.cookieStatus = null;
  }
  async getCookieStatus() {
    if (this.cookieStatus === null) {
      const response = await window.fetch(
        this.statusUrl,
        {
          method: "GET",
          credentials: "same-origin",
          headers: DEFAULT_FETCH_HEADERS
        }
      );
      this.cookieStatus = await response.json();
    }
    if (this.cookieStatus === null) {
      throw new Error("Unexpectedly received null cookie status");
    }
    return this.cookieStatus;
  }
  async saveCookiesStatusBackend(urlProperty) {
    const cookieStatus = await this.getCookieStatus();
    const url = cookieStatus[urlProperty];
    if (!url) {
      throw new Error(`Missing url for ${urlProperty} - was the cookie status not loaded properly?`);
    }
    await window.fetch(url, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        ...DEFAULT_FETCH_HEADERS,
        [this.csrfHeaderName]: cookieStatus.csrftoken
      }
    });
  }
};
var loadCookieGroups = (selector) => {
  const node = document.querySelector(selector);
  if (!node) {
    throw new Error(`No cookie groups (script) tag found, using selector: '${selector}'`);
  }
  return JSON.parse(node.innerText);
};
var doInsertBefore = (beforeNode, newNode) => {
  const parent = beforeNode.parentNode;
  if (parent === null)
    throw new Error("Reference node doesn't have a parent.");
  parent.insertBefore(newNode, beforeNode);
};
var registerEvents = ({
  client,
  cookieBarNode,
  cookieGroups,
  acceptSelector,
  onAccept,
  declineSelector,
  onDecline,
  acceptedCookieGroups: accepted,
  declinedCookieGroups: declined,
  notAcceptedOrDeclinedCookieGroups: undecided
}) => {
  const acceptNode = cookieBarNode.querySelector(acceptSelector);
  if (acceptNode) {
    acceptNode.addEventListener("click", (event) => {
      event.preventDefault();
      const acceptedGroups = filterCookieGroups(cookieGroups, accepted.concat(undecided));
      onAccept == null ? void 0 : onAccept(acceptedGroups, event);
      client.saveCookiesStatusBackend("acceptUrl");
      cookieBarNode.parentNode.removeChild(cookieBarNode);
    });
  }
  const declineNode = cookieBarNode.querySelector(declineSelector);
  if (declineNode) {
    declineNode.addEventListener("click", (event) => {
      event.preventDefault();
      const declinedGroups = filterCookieGroups(cookieGroups, declined.concat(undecided));
      onDecline == null ? void 0 : onDecline(declinedGroups, event);
      client.saveCookiesStatusBackend("declineUrl");
      cookieBarNode.parentNode.removeChild(cookieBarNode);
    });
  }
};
var filterCookieGroups = (cookieGroups, varNames) => {
  return cookieGroups.filter((group) => varNames.includes(group.varname));
};
function cloneNode(node) {
  return node.cloneNode(true);
}
var showCookieBar = async (options = {}) => {
  const {
    templateSelector = "#cookie-consent__cookie-bar",
    cookieGroupsSelector = "#cookie-consent__cookie-groups",
    acceptSelector = ".cookie-consent__accept",
    declineSelector = ".cookie-consent__decline",
    insertBefore = null,
    onShow,
    onAccept,
    onDecline,
    statusUrl = "",
    csrfHeaderName = "X-CSRFToken"
    // Django's default, can be overridden with settings.CSRF_HEADER_NAME
  } = options;
  const cookieGroups = loadCookieGroups(cookieGroupsSelector);
  if (!cookieGroups.length)
    return;
  const templateNode = document.querySelector(templateSelector);
  if (!templateNode) {
    throw new Error(`No (template) element found for selector '${templateSelector}'.`);
  }
  const doInsert = insertBefore === null ? (cookieBarNode2) => document.querySelector("body").appendChild(cookieBarNode2) : typeof insertBefore === "string" ? (cookieBarNode2) => {
    const referenceNode = document.querySelector(insertBefore);
    if (referenceNode === null)
      throw new Error(`No element found for selector '${insertBefore}'.`);
    doInsertBefore(referenceNode, cookieBarNode2);
  } : (cookieBarNode2) => doInsertBefore(insertBefore, cookieBarNode2);
  if (!statusUrl)
    throw new Error("Missing status URL option, did you forget to pass the `statusUrl` option?");
  const client = new FetchClient(statusUrl, csrfHeaderName);
  const cookieStatus = await client.getCookieStatus();
  const {
    acceptedCookieGroups,
    declinedCookieGroups,
    notAcceptedOrDeclinedCookieGroups
  } = cookieStatus;
  const acceptedGroups = filterCookieGroups(cookieGroups, acceptedCookieGroups);
  if (acceptedGroups.length)
    onAccept == null ? void 0 : onAccept(acceptedGroups);
  const declinedGroups = filterCookieGroups(cookieGroups, declinedCookieGroups);
  if (declinedGroups.length)
    onDecline == null ? void 0 : onDecline(declinedGroups);
  if (!notAcceptedOrDeclinedCookieGroups.length)
    return;
  const childToClone = templateNode.content.firstElementChild;
  if (childToClone === null)
    throw new Error("The cookie bar template element may not be empty.");
  const cookieBarNode = cloneNode(childToClone);
  registerEvents({
    client,
    cookieBarNode,
    cookieGroups,
    acceptSelector,
    onAccept,
    declineSelector,
    onDecline,
    acceptedCookieGroups,
    declinedCookieGroups,
    notAcceptedOrDeclinedCookieGroups
  });
  doInsert(cookieBarNode);
  onShow == null ? void 0 : onShow();
};
export {
  loadCookieGroups,
  showCookieBar
};
//# sourceMappingURL=cookiebar.module.js.map
