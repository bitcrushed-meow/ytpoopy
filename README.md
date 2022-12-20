# ytpoopy

Generate hilariously nonsensical videos. Comes with a selection of funny videos that will be cut, rearranged, and warped in various ways to create something entirely new. You can also add your own videos to the mix.


## Dependencies

- Python 3 (made and tested with 3.11)
- FFmpeg (made and tested with 5.1.2 full gyan.dev build)
- VLC (for video playback; output might not play correctly in other video players)


## How to Use

1. Clone this repo:
```shell
git clone https://github.com/m-meowdev/ytpoopy.git ytpoopy/
```

2. Install required Python packages:
```shell
pip install -r requirements.txt
```

3. Optionally, add some of your own videos to the `sources` directory. You can also edit `config.py` and tweak the settings to your liking.

4. Run `main.py`:
```shell
python main.py  # or python3 main.py
```

5. Wait for your video to finish generating. You will find the finished product in the `output` directory.


## To Do

- GUI?
- More effects?

Feel free to suggest any features you want to see!