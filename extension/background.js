const isProdMode = 'update_url' in chrome.runtime.getManifest()
const BACKEND_URL =  isProdMode ? 'TO BE DEFINED' : 'http://127.0.0.1:5000';


function logURL(requestDetails) {
  if (!caught_file && requestDetails.url.includes(".m3u8")) {
    const videoUrl = requestDetails.url;
    console.log(videoUrl, BACKEND_URL);
    chrome.webRequest.onBeforeRequest.removeListener(logURL);
  }
}

// initialize catch variable to "not caught yet"
let caught_file = false;

// listen to all http responses
chrome.webRequest.onBeforeRequest.addListener(logURL, {urls: ["<all_urls>"]});