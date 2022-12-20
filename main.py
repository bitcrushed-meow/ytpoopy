import os
import shutil
import random
import math
import ffmpeg
import config

class Clip:
    def __init__(self, path):
        self.path = path
        self.input = ffmpeg.input(path)
        self.video = self.input.video
        self.audio = self.input.audio
        self.duration = float(ffmpeg.probe(path)["format"]["duration"])
        self.dimensions = int(ffmpeg.probe(path)["streams"][0]["width"]), int(ffmpeg.probe(path)["streams"][0]["height"])
        
clips = []
        
# Get a random number of clips from 'sources' directory.
for root, dirs, files in os.walk("sources"):
    for file in files:
        clips.append(Clip(os.path.join(root, file)))

source_clip_num = random.randint(config.min_source_clip_num, config.max_source_clip_num)
clips = random.sample(clips, k=source_clip_num)

# Cut a random number of subclips from each source clip.
if os.path.isdir("temp"):
    shutil.rmtree("temp")

os.mkdir("temp")

subclips = []

for i, clip in enumerate(clips):
    for x in range(random.randint(config.min_subclip_num, config.max_subclip_num)):
        if config.max_subclip_length > clip.duration:
            subclip_length = random.uniform(config.min_subclip_length, clip.duration)
        else:
            subclip_length = random.uniform(config.min_subclip_length, config.max_subclip_length)

        subclip_start = random.uniform(0, clip.duration - subclip_length)

        subclip_video = clip.video.trim(start=subclip_start, duration=subclip_length).setpts("PTS-STARTPTS")
        subclip_audio = clip.audio.filter("atrim", start=subclip_start, duration=subclip_length).filter("asetpts", "PTS-STARTPTS")
        subclip_output_name = "temp/subclip" + str(i) + "_" + str(x) + ".mp4"
        
        ffmpeg.output(subclip_video, subclip_audio, subclip_output_name).run()
        subclips.append(Clip(subclip_output_name))
        
clips = subclips
            
# Resize all subclips to a consistent size.
clips.sort(reverse=True, key=lambda clip : clip.dimensions[1])

clip_0_width, clip_0_height = clips[0].dimensions

for i, clip in enumerate(clips):
    clip.video = clip.video.filter("scale", width=clip_0_width, height=clip_0_height, force_original_aspect_ratio=1).filter("pad", width=clip_0_width, height=clip_0_height, x="(ow-iw)/2", y="(oh-ih)/2")

# Apply random effects to subclips.
for i, clip in enumerate(clips):
    effects_num = random.randint(config.min_effects, config.max_effects)
    subclip_effects = random.choices(config.effects, k=effects_num)
    
    for effect in subclip_effects:
        if effect == "invert_colors":
            clip.video = clip.video.filter("negate")
        elif effect == "speedx":
            speedx_factor = random.uniform(config.min_speedx_factor, config.max_speedx_factor)
            clip.video = clip.video.setpts("PTS/" + str(speedx_factor))
            clip.audio = clip.audio.filter("atempo", speedx_factor)
        elif effect == "reverse":
            clip.video = clip.video.filter("reverse")
            clip.audio = clip.audio.filter("areverse")
        elif effect == "bitcrush":
            bitcrush_path = clip.path[:-4] + "_bitcrush.mp4"
            ffmpeg.output(clip.video, clip.audio, bitcrush_path, video_bitrate=50000, audio_bitrate=25000).run()
            clips[i] = Clip(bitcrush_path)
        else:
            print("Effect '" + effect + "' does not exist!")
            
# Concatenate all subclips and output resulting video.
def generate_video_name(name):
    """ Returns a unique file name for the output video, using 'name' as a base. """
    
    video_id = 0

    while os.path.exists("output/" + name + str(video_id) + ".mp4"):
        video_id += 1
        
    return "output/" + name + str(video_id) + ".mp4"
        
random.shuffle(clips)

video_output = []
for clip in clips:
    video_output.append(clip.video)
    video_output.append(clip.audio)

ffmpeg.output(ffmpeg.concat(*video_output, v=1, a=1, unsafe=1), generate_video_name("ytp"), fpsmax=60).run()

shutil.rmtree("temp")