# dudakuma
## Lip Reading in Turkish

The main reason that we have declared to start this project is, we have
recognized that lip reading tools are available in most of the popular
languages but not in our own language. So that, we came up with an idea
that can be helpful for Turkish people with disabilities. We believe that Lip
Reading in Turkish will also be helpful for developers who wants to study
in this area.

## Features

- For our current progress, we can state that our dataset consists of more than 12500 frames extracted from 522 different media files. 
- In addition, our dataset has the capability of detecting approximately 102 Turkish words (including Turkish special characters) based on lip detection, extraction, and frame creation processes. 
- For future work, our database content is completely ready for upcoming training purposes. We are planning to share and distribute our progress with developers who are ready and eager to work on lip-reading functionalities in Turkish.
- For demo purposes or if you want to skip the dataset creation and working on algorithms, please reach us out. We will be happy to share our dataset.

## Tech

dudakuma uses a number of open source libraries to work properly:

- [Python] 
- [Pandas]
- [Imutils]
- [Numpy]
- [Dlib]
- [OpenCV]
- [tqdm]
- [PIL]
- [MatPlotLib]
- [Youtube-Dl]
- [csv]
- [os]
- [glob]
- [datetime]
- [re]

## Execution

Execution order of the dataset creation of dudakuma:

```sh
1. CSV Generation/dataset_yt_channel_subtitle_downloader.py
2. CSV Generation/dataset_most_common_word_finder.py
3. CSV Generation/dataset_generator.py
```

For preprocess applications...

```sh
4. Model Preprocessing/model_dataset_video_downloader.py
5. Model Preprocessing/model_dataset_video_cutter.py
6. Model Preprocessing/model_dataset_video_preprocessor.py
```

## License

MIT


   [os]: <https://docs.python.org/3/library/os.html>
   [git-repo-url]: <https://github.com/tunacinsoy/dudakuma.git>
   [os]: <http://daringfireball.net>
   [csv]: <https://docs.python.org/3/library/csv.html>
   [Youtube-DL]: <https://youtube-dl.org/>
   [MatPlotLib]: <https://matplotlib.org/>
   [PIL]: <https://pillow.readthedocs.io/en/stable/>
   [tqdm]: <https://tqdm.github.io/>
   [OpenCV]: <https://pypi.org/project/opencv-python/>
   [Dlib]: <http://dlib.net/>
   [Numpy]: <https://numpy.org/>
   [Imutils]: <https://pypi.org/project/imutils/>
   [Python]: <https://www.python.org/>
   [Pandas]: <https://pandas.pydata.org/>
   [Glob]: <https://docs.python.org/3/library/glob.html>
   [datetime]: <https://docs.python.org/3/library/datetime.html>
   [re]: <https://docs.python.org/3/library/re.html>
   [Glob]: <https://docs.python.org/3/library/glob.html>
   
