console.log("Hi from chrome extension");
// 117017-004-A_v720.mp4
// 117017-004-A_aud_VF-FRA_1.mp4
function logURL(requestDetails) {
    if (requestDetails.url.includes("A_v720.mp4")) {
        // console.log(`Loading video: ${requestDetails.url}`);
        const videoUrl = requestDetails.url;
        document.dispatchEvent(new CustomEvent("video", { detail: videoUrl }));
    } else if (requestDetails.url.includes("A_aud_VF-FRA_1.mp4")) {
        // console.log(`Loading audio: ${requestDetails.url}`);
        const audioUrl = requestDetails.url;
        document.dispatchEvent(new CustomEvent("audio", { detail: audioUrl }));
    } else {
        return;
    }
}

chrome.webRequest.onBeforeRequest.addListener(logURL, {
urls: ["<all_urls>"],
});

const videoPromise = new Promise((resolve, reject) => {
    document.addEventListener("video", (e) => resolve(e.detail))
});
const audioPromise = new Promise((resolve, reject) => {
    document.addEventListener("audio", (e) => resolve(e.detail))
});

Promise.all([videoPromise, audioPromise]).then((urls) => {
  const [videoUrl, audioUrl] = urls;
  console.log(videoUrl, audioUrl, urls);
});
