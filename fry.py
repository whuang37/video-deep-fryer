import ffmpeg
import random
import os # for emoji parsing
import argparse

emoji_folder = "emoji/"

def parse_args():
    ap = argparse.ArgumentParser()

    ap.add_argument("-iv", "--input_video", help="input video")
    ap.add_argument("-ia", "--input_audio", help="input audio")
    ap.add_argument("-o", "--output_file", help="output file")
    ap.add_argument("-nv", "--n_video", help="number of times to process video", default=2, type=int)
    ap.add_argument("-na", "--n_audio", help="number of times to process audio", default=1, type=int)
    ap.add_argument("-ne", "--n_emojis", help="number of emojis to add", default=20, type=int)
    args = ap.parse_args()
    return args

def get_metadata(v_path):


    probe_data_streams = ffmpeg.probe(v_path)["streams"]
    
    for probe_data in probe_data_streams:
        if "width" in probe_data:
            dimensions = (int(probe_data["width"]), int(probe_data["height"]))
        if "duration" in probe_data:
            duration = float(probe_data["duration"])

    return dimensions, duration

def overlay_emojis(v, n_emojis, dimension, duration):
    emojis = os.listdir(emoji_folder)
    selected_emojis = random.choices(emojis, k=n_emojis)
    selected_emojis = [os.path.join(emoji_folder, path) for path in selected_emojis] # gets full relative path

    max_emoji_size = int(dimension[0]/3) if dimension[0]/3 < dimension[1]/3 else int(dimension[1]/3) #ensure one emoji isnt too big
    for emoji in selected_emojis:
        emoji_stream = ffmpeg.input(emoji)
    
        emoji_size = random.randint(10, max_emoji_size)
        emoji_angle = random.uniform(0, 6.28)

        emoji_stream = emoji_stream.filter("scale", emoji_size, emoji_size)
        emoji_stream = emoji_stream.filter("rotate", emoji_angle)

        emoji_x = random.randint(0, dimension[0])
        emoji_y = random.randint(0, dimension[1])
        emoji_start = random.uniform(0, duration-1.4)
        emoji_end = random.uniform(emoji_start+1, duration)

        v = v.overlay(emoji_stream, 
                      x=emoji_x, 
                      y=emoji_y, 
                      enable=f"between(t, {emoji_start}, {emoji_end})")

    return v

def filter_audio(a):
    a = a.filter("aecho", .7, .4, 200, .3)

    a = a.filter("acrusher", bits=16, samples=64)
    a = a.filter("acompressor", threshold=.08, attack=.01, release=.01)
    
    a = a.filter("volume", "30dB")
    a = a.filter("treble", gain=-10)
    a = a.filter("bass", gain=13)

    return a

def filter_video(v):
    # setting values
    saturation = random.uniform(3,5)
    contrast = random.uniform(1, 3)
    g_r = random.uniform(1, 3)
    g_b = random.uniform(1, 2)
    g_g = random.uniform(1, 3)

    noise = random.uniform(3, 7)
    v = v.filter("noise",
                 alls=noise,
                 allf="t") # temporal noise

    # saturation/contrast/gammas
    v = v.filter("eq", 
                 saturation=saturation,
                 contrast=contrast,
                 gamma_r=g_r,
                 gamma_b=g_b,
                 gamma_g=g_g)

    # emboss video
    emboss_string = "-2 -1 0 -1 1 1 0 1 2",
    v = v.filter("convolution",
                emboss_string,
                emboss_string,
                emboss_string,
                emboss_string
                )

    # sharpen video
    v = v.filter("unsharp",
                lx=5,
                ly=5,
                la=1.25,
                cx=5,
                cy=5,
                ca=1)
    return v

def main():
    args = parse_args()
    stream = ffmpeg.input(args.input_video)
    dimension, duration = get_metadata(args.input_video)

    v = stream.video
    if args.input_audio != None:
        audio_stream = ffmpeg.input(args.input_audio)
        audio_stream = audio_stream.audio
    else:
        a = stream.audio


    for i in range(args.n_video):
        v = filter_video(v)
        if i == args.n_video - 1:
            v = overlay_emojis(v, args.n_emojis, dimension, duration)
    
    for _ in range(args.n_audio):
        a = filter_audio(a)

    out = ffmpeg.output(v, a, "data/out.mp4", 
                        loglevel="warning", 
                        shortest=None, 
                        video_bitrate="500k", 
                        audio_bitrate="100k")
    print(out.get_args())
    out.run()


if __name__ == "__main__":
    main()