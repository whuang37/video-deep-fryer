import ffmpeg
import random

def filter_audio(a):
    #acompressor
    # acrusher
    # aecho
    # apad
    # asubboost
    # dynaudnorm
    # 
    pass        



def filter_video(v):
    # setting values
    saturation = random.uniform(3,5)
    contrast = random.uniform(1, 3)
    g_r = random.uniform(1, 3)
    g_b = random.uniform(1, 3)
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
    stream = ffmpeg.input('data/test.mov')
    v_final = stream.video
    a_final = stream.audio

    v_final = filter_video(v_final)
    v_final = filter_video(v_final)
    out = ffmpeg.output(v_final, a_final, "data/out.mp4", loglevel="warning")
    print(out.get_args())
    out.run()


if __name__ == "__main__":
    main()