function logURL(requestDetails) {
  if (!caught_file && requestDetails.url.includes(".m3u8")) {
    const videoUrl = requestDetails.url;
    console.log(videoUrl);
    chrome.webRequest.onBeforeRequest.removeListener(logURL);
  }
}

// initialize catch variable to "not caught yet"
let caught_file = false;

// listen to all http responses
chrome.webRequest.onBeforeRequest.addListener(logURL, {urls: ["<all_urls>"]});