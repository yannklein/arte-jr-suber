const isProdMode = 'update_url' in chrome.runtime.getManifest()
const BACKEND_URL =  isProdMode ? 'TO BE DEFINED' : 'http://127.0.0.1:8000';

const form = document.querySelector(".subbing-form");
const formVideoContainer = document.querySelector(".form-videos");
const submitButton = document.querySelector(".subbing-button");
const inProgress = document.querySelector(".in-progress");
const timeSpan = document.querySelector(".subbing-time");
const downloadBtn = document.querySelector(".download-button");
const reset = document.querySelector(".reset");

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

// listen to form submit to start subbing
const enableFormSubmit = () => {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    updateDisplay('inProgress');

    const inForty = new Date(new Date().getTime() + 40*60000);
    updateTime(inForty)
    setInterval(() => { updateTime(inForty) }, 60000);

    const reqUrl = form.elements[0].name;
    const reqLang = form.elements[1].value;

    // send the url to the backend
    const url = `${BACKEND_URL}?url=${reqUrl}&lang=${reqLang}`;
    const response = await fetch(url);
    const file_urls = await response.json();

    updateDisplay('finished');
    
    // const file_urls = {'final_video': "test"}
    downloadBtn.addEventListener("click", () => {
      const newURL = `${BACKEND_URL}/${file_urls['final_video']}`;
      chrome.tabs.create({ url: newURL });
    })
    reset.addEventListener("click", () => {
      updateDisplay('initial');
    })

  })
}

const updateTime = (inForty) => {
  localStorage.setItem("inForty", inForty)
  if (!inForty) {
    return
  }
  let diff = Math.floor((new Date(inForty) - new Date())/60000);
  if (diff < 0 ) {
    diff = 0;
  }
  timeSpan.innerHTML = diff;
}

const updateDisplay = (status) => {
  switch (status) {
    case "inProgress":
      localStorage.setItem("status", 'inProgress');
      submitButton.classList.add("d-none");
      inProgress.classList.remove("d-none");
      break;
    case "finished":
      localStorage.setItem("status", 'finished');
      form.classList.add("d-none");
      inProgress.classList.add("d-none");
      downloadBtn.parentElement.classList.remove("d-none");
      break;
  
    default:
      localStorage.setItem("status", 'initial');
      form.classList.remove("d-none");
      submitButton.classList.remove("d-none");
      downloadBtn.parentElement.classList.add("d-none");
      break;
  }
}

// check and keep track of status even when chrome extension closed
updateTime(localStorage.getItem("inForty"));
updateDisplay(localStorage.getItem("status"));

// listen to all http responses
chrome.webRequest.onBeforeRequest.addListener(logURL, {urls: ["<all_urls>"]});

