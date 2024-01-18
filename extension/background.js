const isProdMode = 'update_url' in chrome.runtime.getManifest()
const BACKEND_URL =  isProdMode ? 'TO BE DEFINED' : 'http://127.0.0.1:5000';


async function logURL(requestDetails) {
  const reqUrl = requestDetails.url;
  if (reqUrl.includes(".m3u8")) {
    // stop logging http responses when the first is caught
    chrome.webRequest.onBeforeRequest.removeListener(logURL);
    // send the url to the backend
    const response = await fetch(`${BACKEND_URL}?url=${reqUrl}`);
    const file_url = await response.json();
    // display url of translated video
    console.log(file_url);
  }
}

// listen to all http responses
chrome.webRequest.onBeforeRequest.addListener(logURL, {urls: ["<all_urls>"]});