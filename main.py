import os
import shutil
import random
import math
import ffmpeg
import config

class Clip:
    def __init__(self, path):
        self.input = ffmpeg.input(path)
        self.video = self.input.video
        self.audio = self.input.audio
        self.duration = float(ffmpeg.probe(path)["format"]["duration"])
        self.dimensions = int(ffmpeg.probe(path)["streams"][0]["width"]), int(ffmpeg.probe(path)["streams"][0]["height"])
        
# Get a random number of clips from 'sources' directory.
source_clips = []

for root, dirs, files in os.walk("sources"):
    for file in files:
        source_clips.append(Clip(os.path.join(root, file)))

source_clip_num = random.randint(config.min_source_clip_num, config.max_source_clip_num)
source_clips = random.sample(source_clips, k=source_clip_num)

# Cut a random number of subclips from each source clip.
if not os.path.isdir("temp"):
    os.mkdir("temp")

subclips = []

for i, clip in enumerate(source_clips):
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
            
# Resize all subclips to a consistent size.
subclips.sort(reverse=True, key=lambda clip : clip.dimensions[1])

resized_clips = []

clip_0_width, clip_0_height = subclips[0].dimensions

for i, clip in enumerate(subclips):
    clip_video_resized = clip.video.filter("scale", width=clip_0_width, height=clip_0_height, force_original_aspect_ratio=1).filter("pad", width=clip_0_width, height=clip_0_height, x="(ow-iw)/2", y="(oh-ih)/2")
    clip_output_name = "temp/resized" + str(i) + ".mp4"

    ffmpeg.output(clip_video_resized, clip.audio, clip_output_name).run()
    resized_clips.append(Clip(clip_output_name))

subclips = resized_clips

# Apply random effects to subclips.
effects_clips= []

for i, clip in enumerate(subclips):
    effects_num = random.randint(config.min_effects, config.max_effects)
    subclip_effects = random.choices(config.effects, k=effects_num)
    
    subclip_video = clip.video
    subclip_audio = clip.audio
    subclip_output_name = "temp/effects" + str(i) + ".mp4"

    for effect in subclip_effects:
        if effect == "invert_colors":
            subclip_video = subclip_video.filter("negate")
        elif effect == "speedx":
            speedx_factor = random.uniform(config.min_speedx_factor, config.max_speedx_factor)
            subclip_video = subclip_video.setpts("PTS/" + str(speedx_factor))
            subclip_audio = subclip_audio.filter("atempo", speedx_factor)
        elif effect == "reverse":
            subclip_video = subclip_video.filter("reverse")
            subclip_audio = subclip_audio.filter("areverse")
        else:
            print("Effect '" + effect + "' does not exist!")
            
    ffmpeg.output(subclip_video, subclip_audio, subclip_output_name).run()
    effects_clips.append(Clip(subclip_output_name))
    
subclips = effects_clips
                
def generate_video_name(name):
    """ Returns a unique file name for the output video, using 'name' as a base. """
    
    video_id = 0

    while os.path.exists("output/" + name + str(video_id) + ".mp4"):
        video_id += 1
        
    return "output/" + name + str(video_id) + ".mp4"
        
# Concatenate all subclips and output resulting video.
random.shuffle(subclips)

video_output = []
for clip in subclips:
    video_output.append(clip.video)
    video_output.append(clip.audio)

ffmpeg.output(ffmpeg.concat(*video_output, v=1, a=1, unsafe=1), generate_video_name("ytp"), fpsmax=60).run()

shutil.rmtree("temp")