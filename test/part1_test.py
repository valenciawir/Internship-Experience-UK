import re
from src.video_player import VideoPlayer


def test_number_of_videos(capfd):
    player = VideoPlayer()
    player.number_of_videos()
    out, err = capfd.readouterr()
    assert "5 videos in the library" in out




    def show_all_videos(self):
        """Returns all videos."""
        all_videos = self._video_library.get_all_videos()  # Fetch all the videos, based off above function
        all_videos.sort(key=lambda x: x.title)  # Use key with lambda to dictate sort to only go through video title
        print("Here's a list of all available videos:")

        for video in all_videos:  # Loop through txt file, reading each video line by line
            tagString = str(video.tags)  # Convert to string to allow stripping of brackets
            # tagStrip.strip("()") # Old code - this didn't make a difference with this line placement
            print(video.title, "(", video.video_id, ")", "[", tagString.strip("()"), "]")

        # print("show_all_videos needs implementation")


    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """

        vidPlay = self._video_library.get_video(video_id)  # Start playing the chosen video

        try:  # Check if the video exists
            vidPlay.video_id
        except AttributeError:  # If video doesn't exist, don't bother with the rest of the code
            print("Cannot play video: Video does not exist")
        else:  # Continue as normal if the video exists
            # print("Current ID:", vidPlay.video_id) # Debug
            # currentVideo = vidPlay  # Old code with local currentVideo variable. Caused too much headaches to work
            if self.isPlaying:  # Don't this message on first run of function
                print("Stopping video:", self.currentVideo.title)  # Stop the previous video if any
                self.isPaused = False
            print("Playing video:", vidPlay.title)
            self.isPlaying = True
            self.currentVideo = vidPlay  # Store the video currently playing in a variable

        # print("play_video needs implementation")

def test_play_video_nonexistent(capfd):
    player = VideoPlayer()
    player.play_video("does_not_exist")
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 1
    assert "Cannot play video: Video does not exist" in out


def test_play_video_stop_previous(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.play_video("funny_dogs_video_id")
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 3
    assert "Playing video: Amazing Cats" in lines[0]
    assert "Stopping video: Amazing Cats" in lines[1]
    assert "Playing video: Funny Dogs" in lines[2]


def test_play_video_dont_stop_previous_if_nonexistent(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.play_video("some_other_video")
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 2
    assert "Playing video: Amazing Cats" in lines[0]
    assert "Stopping video: Amazing Cats" not in out
    assert "Cannot play video: Video does not exist" in lines[1]


def test_stop_video(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.stop_video()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 2
    assert "Playing video: Amazing Cats" in lines[0]
    assert "Stopping video: Amazing Cats" in lines[1]

    def stop_video(self):
        """Stops the current video."""
        if self.isPlaying is True:
            print("Stopping video:", self.currentVideo.title)
            self.isPlaying = False
            self.isPaused = False
        else:
            print("Cannot stop video: No video is currently playing")

        # print("stop_video needs implementation")

def test_stop_video_twice(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.stop_video()
    player.stop_video()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 3
    assert "Playing video: Amazing Cats" in lines[0]
    assert "Stopping video: Amazing Cats" in lines[1]
    assert "Cannot stop video: No video is currently playing" in lines[2]


def test_stop_video_none_playing(capfd):
    player = VideoPlayer()
    player.stop_video()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 1
    assert "Cannot stop video: No video is currently playing" in out


def test_play_random_video(capfd):
    player = VideoPlayer()
    player.play_random_video()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 1
    assert re.match(
        "Playing video: (Amazing Cats|Another Cat Video|Funny Dogs|Life at Google|Video about nothing)",
        out)


def test_play_random_stops_previous_video(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.play_random_video()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 3
    assert "Playing video: Amazing Cats" in lines[0]
    assert "Stopping video: Amazing Cats" in lines[1]
    assert re.match(
        "Playing video: (Amazing Cats|Another Cat Video|Funny Dogs|Life at Google|Video about nothing)",
        lines[2])


def test_show_playing(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.show_playing()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 2
    assert "Playing video: Amazing Cats" in lines[0]
    assert "Currently playing: Amazing Cats (amazing_cats_video_id) [#cat #animal]" in lines[1]


def test_show_nothing_playing(capfd):
    player = VideoPlayer()
    player.show_playing()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 1
    assert "No video is currently playing" in lines[0]


def test_pause_video(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.pause_video()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 2
    assert "Playing video: Amazing Cats" in lines[0]
    assert "Pausing video: Amazing Cats" in lines[1]


def test_pause_video_show_playing(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.pause_video()
    player.show_playing()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 3
    assert "Currently playing: Amazing Cats (amazing_cats_video_id) " \
           "[#cat #animal] - PAUSED" in lines[2]


def test_pause_video_play_video(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.pause_video()
    player.play_video("amazing_cats_video_id")
    player.show_playing()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 5
    assert "Playing video: Amazing Cats" in lines[0]
    assert "Pausing video: Amazing Cats" in lines[1]
    assert "Stopping video: Amazing Cats" in lines[2]
    assert "Playing video: Amazing Cats" in lines[3]
    assert "Currently playing: Amazing Cats (amazing_cats_video_id) " \
           "[#cat #animal]" in lines[4]
    assert "PAUSED" not in lines[4]


def test_pause_already_paused_video(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.pause_video()
    player.pause_video()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 3
    assert "Playing video: Amazing Cats" in lines[0]
    assert "Pausing video: Amazing Cats" in lines[1]
    assert "Video already paused: Amazing Cats" in lines[2]


def test_pause_video_none_playing(capfd):
    player = VideoPlayer()
    player.pause_video()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 1
    assert "Cannot pause video: No video is currently playing" in lines[0]


def test_continue_video(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.pause_video()
    player.continue_video()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 3
    assert "Playing video: Amazing Cats" in lines[0]
    assert "Pausing video: Amazing Cats" in lines[1]
    assert "Continuing video: Amazing Cats" in lines[2]


def test_continue_video_not_paused(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.continue_video()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 2
    assert "Cannot continue video: Video is not paused" in lines[1]


def test_continue_none_playing(capfd):
    player = VideoPlayer()
    player.continue_video()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 1
    assert "Cannot continue video: No video is currently playing" in lines[0]
