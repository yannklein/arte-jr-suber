const isProdMode = 'update_url' in chrome.runtime.getManifest()
const BACKEND_URL =  isProdMode ? 'TO BE DEFINED' : 'http://127.0.0.1:5000';


async function logURL(requestDetails) {
  const reqUrl = requestDetails.url;
  if (reqUrl.includes(".m3u8")) {
    // stop logging http responses when the first is caught
    chrome.webRequest.onBeforeRequest.removeListener(logURL);
    //display found videos
    const formVideoContainer = document.querySelector(".form-videos");
    const button = `
      <input type="radio" class="btn-check" name="videos" id="video1" autocomplete="off">
      <label class="btn btn-outline-danger" for="video1">Arte Journal</label>
    `;
    formVideoContainer.innerHTML = "";
    formVideoContainer.insertAdjacentHTML("afterbegin", button);
    // enable form submission
    enableFormSubmit();
  }
}

// listen to all http responses
chrome.webRequest.onBeforeRequest.addListener(logURL, {urls: ["<all_urls>"]});

// listen to form submit to start subbing
 const enableFormSubmit = () => {
  const form = document.querySelector(".subbing-form");
  form.addEventListener("submit", async (event) => {
    console.log(form);
    // send the url to the backend
    const response = await fetch(`${BACKEND_URL}?url=${reqUrl}`);
    const file_url = await response.json();
    // display url of translated video
    console.log(file_url);
  })
}