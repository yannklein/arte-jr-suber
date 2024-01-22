const isProdMode = 'update_url' in chrome.runtime.getManifest()
const BACKEND_URL =  isProdMode ? 'TO BE DEFINED' : 'http://127.0.0.1:4000';

const form = document.querySelector(".subbing-form");
const formVideoContainer = document.querySelector(".form-videos");
const submitButton = document.querySelector(".subbing-button");
const inProgress = document.querySelector(".in-progress");
const timeSpan = document.querySelector(".subbing-time");
const downloadBtn = document.querySelector(".download-button");
const resets = document.querySelectorAll(".reset");
const error = document.querySelector(".error");

async function logURL(requestDetails) {
  const reqUrl = requestDetails.url;
  if (reqUrl.includes(".m3u8")) {
    // stop logging http responses when the first is caught
    chrome.webRequest.onBeforeRequest.removeListener(logURL);
    //display found videos
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

const updateTime = (inForty) => {
  localStorage.setItem("inForty", inForty)
  if (!inForty) {
    return
  }
  setInterval(() => { updateTime(localStorage.getItem("inForty")) }, 60000);
  let diff = Math.floor((new Date(inForty) - new Date())/60000);
  if (diff < 0 ) {
    diff = 0;
    updateDisplay("finished"); // TODO: tackle the false positive problem
  }
  timeSpan.innerHTML = diff;
}

const updateDisplay = (status) => {

  // hide all
  submitButton.classList.add("d-none");
  form.classList.add("d-none");
  inProgress.classList.add("d-none");
  error.classList.add("d-none");
  downloadBtn.parentElement.classList.add("d-none");

  switch (status) {
    case "inProgress":
      localStorage.setItem("status", 'inProgress');
      form.classList.remove("d-none");
      inProgress.classList.remove("d-none");
      break;
    case "finished":
      localStorage.setItem("status", 'finished');
      downloadBtn.parentElement.classList.remove("d-none");
      break;

    case "error":
      localStorage.setItem("status", 'error');
      error.classList.remove("d-none");
      break;
  
    default:
      localStorage.setItem("status", 'initial');
      form.classList.remove("d-none");
      submitButton.classList.remove("d-none");
      break;
  }
}

// listen to form submit to start subbing
const enableFormSubmit = () => {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    updateDisplay('inProgress');

    const inForty = new Date(new Date().getTime() + 40*60000);
    updateTime(inForty)

    const reqUrl = form.elements[0].name;
    const reqLang = form.elements[1].value;

    // send the url to the backend
    const url = `${BACKEND_URL}?url=${reqUrl}&lang=${reqLang}`;
    try {
      const response = await fetch(url);
      if (!res.ok) {
        throw new ResponseError('Bad fetch response', res);
      }
      const file_urls = await response.json();
      updateDisplay('finished');
    } catch(err) {
      updateDisplay('error');  
    }

  })
}

downloadBtn.addEventListener("click", () => {
  const newURL = `${BACKEND_URL}/videos/translated.mp4`;
  chrome.tabs.create({ url: newURL });
})

resets.forEach( reset => {
  reset.addEventListener("click", () => {
    updateDisplay('initial');
  })
});

// check and keep track of status even when chrome extension closed
updateTime(localStorage.getItem("inForty"));
updateDisplay(localStorage.getItem("status"));

// listen to all http responses
chrome.webRequest.onBeforeRequest.addListener(logURL, {urls: ["<all_urls>"]});

