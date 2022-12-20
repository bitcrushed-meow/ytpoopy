min_source_clip_num = 5   # minimum number of source clips to be used
max_source_clip_num = 10  # maximum number of source clips to be used

min_subclip_length = 1  # minimum length each subclip can be (in seconds)
max_subclip_length = 5  # maximum length each subclip can be (in seconds)

min_subclip_num = 1  # minimum number of subclips to be generated per source clip
max_subclip_num = 5  # maximum number of subclips to be generated per source clip

min_effects = 0  # minimum number of video effects that can be applied to a subclip
max_effects = 2  # maximum number of video effects that can be applied to a subclip

effects = ["invert_colors", "speedx", "reverse", "bitcrush"]  # effects that can be applied to subclips

min_speedx_factor = 0.5  # minimum factor by which a subclip can be sped up or slowed down
max_speedx_factor = 2    # maximum factor by which a subclip can be sped up or slowed down