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
      <input type="radio" class="btn-check" name="${reqUrl}" id="video1" autocomplete="off">
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
    event.preventDefault();
    const submitButton = document.querySelector(".subbing-button");
    submitButton.disabled = true;
    submitButton.innerHTML = `
    <div class="d-flex flex-column align-items-center mt-2">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p>Generating subtitles...</p>
    </div>
    `;
    const reqUrl = form.elements[0].name;
    const reqLang = form.elements[1].value;
    // send the url to the backend
    const url = `${BACKEND_URL}?url=${reqUrl}&lang=${reqLang}`;
    const response = await fetch(url);
    const file_url = await response.json();
    // display url of translated video
    console.log(file_url);
  })
}