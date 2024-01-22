<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="https://github.com/yannklein/arte-jr-suber/assets/26819547/f60e07fd-ed65-487f-b956-7353ebd3312f" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Video stream subber chrome extension</h3>

  <p align="center">
    A Chrome extension that gets a website video stream and subtitles it in any language. 
    <br />
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Report Bug</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#demo">Demo</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

The project consist of a Chrome extension that gets a website video stream and sends it to a Python backend which generates its subtitle in any other language and output the subtitled video. 
I used it to add subtitles to my favorite TV news: <a href='https://www.arte.tv/fr/videos/RC-014085/arte-journal/'>Arte Journal</a>.
<kbd>  
  <img width="299" alt="image" src="https://github.com/yannklein/arte-jr-suber/assets/26819547/5a1cb198-b7e2-4759-a173-ea5d97fb838a">
</kbd>

This project is a pipepline of different processes as follows:
1. The Chrome Extension detects HTTP reponses containing .m3u8 stream payloads and send it to the project's backend
2. The stream is turned into a video and audio file using the [ffmpeg-python](https://pypi.org/project/ffmpeg-python/) library
3. The audio file is transformed into timed transcripts using openAI's [whisper](https://pypi.org/project/openai-whisper/)
4. The transcript is translated in the target language using [Google Translate](https://cloud.google.com/translate/docs/reference/libraries/v2/python)
5. The translated transcript is merged to the original video as subtitles using the [ffmpeg-python](https://pypi.org/project/ffmpeg-python/) library

The whole process take around 40min for a 20min video.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With
* [![Python][Python]][Python-url]
* [![Flask][Flask]][Flask-url]
* [![ffmpeg][ffmpeg]][ffmpeg-url]
* [![chrome][chrome]][chrome-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Demo
https://github.com/yannklein/arte-jr-suber/assets/26819547/faba338b-176d-4d88-a335-7ef2e7e04896



<!-- GETTING STARTED -->

### Prerequisites

This project needs a environment with Python and `pip`.

### Installation

1. Load the `extension` folder in Chrome following [these steps](https://support.google.com/chrome_webstore/answer/2664769?hl=en)
2. Install python packages using the Makefile command:
   ```sh
   make install
   ```
3. Run the backend with the Makefile command:
   ```sh
   make dev-run
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Check and follow the steps of the video <a href="#demo">Demo</a>.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Build the basic pipeline
- [ ] Adapt frontend for any video stream
- [ ] Add websocket for front/back end communication
- [ ] Adapt project for multiple users
- [ ] Store assets on cloud services
- [ ] Improve processing speed


See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* Thanks to [Tomo](https://github.com/tomozilla) for inspiring and hinting way to build this project
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=FFE466
[Python-url]: https://www.python.org
[ffmpeg]: https://img.shields.io/badge/ffmpeg-007808?style=for-the-badge&logo=ffmpeg&logoColor=black
[ffmpeg-url]: https://ffmpeg.org
[chrome]: https://img.shields.io/badge/Chrome%20Extension-lightgray?style=for-the-badge&logo=googlechrome&logoColor=FC521F
[chrome-url]: https://chromewebstore.google.com
[Flask]: https://img.shields.io/badge/flask-black?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/en/3.0.x/
