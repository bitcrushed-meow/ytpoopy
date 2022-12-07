import os
import random
import math
from moviepy.editor import *

min_subclip_length = 1  # minimum length each subclip can be (in seconds)
max_subclip_length = 5  # maximum length each subclip can be (in seconds)

min_subclip_num = 1 # minimum number of subclips to be generated per source clip
max_subclip_num = 5 # maximum number of subclips to be generated per source clip

min_video_effects = 0 # minimum number of video effects that can be applied to a subclip
max_video_effects = 2 # maximum number of video effects that can be applied to a subclip

video_effects = ["invert_colors", "speedx", "time_mirror", "time_symmetrize"] # video effects to be applied to subclips

min_speedx_factor = 0.25 # minimum factor by which a subclip can be sped up or slowed down
max_speedx_factor = 4    # maximum factor by which a subclip can be sped up or slowed down

# get each video in source folder
source_clips = []

for root, dirs, files in os.walk("sources"):
    for file in files:
        source_clips.append(VideoFileClip(os.path.join(root, file)))
        
# resize source clips to a consistent size
source_clips.sort(reverse=True, key=lambda clip : clip.h)

for i in range(len(source_clips)):
    source_clips[i] = source_clips[i].resize(height=source_clips[0].h)
        
# cut each source clip into random subclips
subclips = []

for clip in source_clips:
    for x in range(random.randint(min_subclip_num, max_subclip_num)):
        if max_subclip_length > clip.duration:
            subclip_length = random.uniform(min_subclip_length, clip.duration)
        else:
            subclip_length = random.uniform(min_subclip_length, max_subclip_length)

        subclip_start = random.uniform(min_subclip_length, clip.duration - subclip_length)
        subclips.append(clip.subclip(subclip_start, subclip_start + subclip_length))
        
# apply random effects to subclips
for i in range(len(subclips)):
    video_effects_num = random.randint(min_video_effects, max_video_effects)
    subclip_video_effects = random.choices(video_effects, k=video_effects_num)
    for effect in subclip_video_effects:
        if effect == "invert_colors":
            subclips[i] = subclips[i].invert_colors()
        elif effect == "speedx":
            subclips[i] = subclips[i].speedx(factor=random.uniform(min_speedx_factor, max_speedx_factor))
        elif effect == "time_mirror":
            subclips[i] = subclips[i].fx(vfx.time_mirror)
        elif effect == "time_symmetrize":
            subclips[i] = subclips[i].fx(vfx.time_symmetrize)
        else:
            print("Effect '" + effect + "' does not exist!")
        
# put together + output final video
random.shuffle(subclips)
video_output = concatenate_videoclips(subclips, method="compose")
video_output.write_videofile("output/ytp.mp4")