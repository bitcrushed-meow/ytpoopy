import os
import random
import math
import moviepy.editor as mpy
import config

def generate_source_clips():
    """ Returns a list of VideoFileClips containing a random amount of videos in directory 'sources'. """

    source_clips = []

    for root, dirs, files in os.walk("sources"):
        for file in files:
            source_clips.append(mpy.VideoFileClip(os.path.join(root, file)))

    source_clip_num = random.randint(config.min_source_clip_num, config.max_source_clip_num)
    return random.choices(source_clips, k=source_clip_num)
        
def resize_clips(clips):
    """ Resizes all clips in list 'clips' to be the same height as the clip with the largest height while maintaining aspect ratio. """

    clips.sort(reverse=True, key=lambda clip : clip.h)

    for i in range(len(clips)):
        clips[i] = clips[i].resize(height=clips[0].h)
        
def cut_clips(clips):
    """ Returns a list containing a random amount of subclips of random length cut from each clip in list 'clips'. """

    subclips = []

    for clip in clips:
        for x in range(random.randint(config.min_subclip_num, config.max_subclip_num)):
            if config.max_subclip_length > math.floor(clip.duration):
                subclip_length = random.uniform(config.min_subclip_length, math.floor(clip.duration))
            else:
                subclip_length = random.uniform(config.min_subclip_length, config.max_subclip_length)

            subclip_start = random.uniform(config.min_subclip_length, math.floor(clip.duration) - subclip_length)
            subclips.append(clip.subclip(subclip_start, subclip_start + subclip_length))
            
    return subclips
        
def apply_video_effects(clips):
    """ Applies a random amount of video effects to each clip in list 'clips'. """

    for i in range(len(clips)):
        video_effects_num = random.randint(config.min_video_effects, config.max_video_effects)
        subclip_video_effects = random.choices(config.video_effects, k=video_effects_num)

        for effect in subclip_video_effects:
            if effect == "invert_colors":
                clips[i] = clips[i].invert_colors()
            elif effect == "speedx":
                clips[i] = clips[i].speedx(factor=random.uniform(config.min_speedx_factor, config.max_speedx_factor))
            elif effect == "time_mirror":
                clips[i] = clips[i].fx(mpy.vfx.time_mirror)
            elif effect == "time_symmetrize":
                clips[i] = clips[i].fx(mpy.vfx.time_symmetrize)
            else:
                print("Effect '" + effect + "' does not exist!")
                
def generate_video_name(name):
    """ Returns a unique file name for the output video, using 'name' as a base. """
    
    video_id = 0

    while os.path.exists("output/" + name + str(video_id) + ".mp4"):
        video_id += 1
        
    return "output/" + name + str(video_id) + ".mp4"
        
def compile_video(clips):
    """ Compiles all clips in list 'clips' together in a random order and outputs the resulting video. """

    random.shuffle(clips)
    video_output = mpy.concatenate_videoclips(clips, method="compose")
    video_output.write_videofile(generate_video_name("ytp"))
    
source_clips = generate_source_clips()
resize_clips(source_clips)

subclips = cut_clips(source_clips)
apply_video_effects(subclips)
compile_video(subclips)