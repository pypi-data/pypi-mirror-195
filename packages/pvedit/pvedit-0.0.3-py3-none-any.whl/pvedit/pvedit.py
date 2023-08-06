import click 
import numpy as np
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip, afx, concatenate_videoclips


@click.command()
@click.argument('filename', required=True, type=click.Path(exists=True))
@click.option('--graph', '-g', default=False, is_flag=True, help="Plot the graphs")
@click.option('--verbose', '-v', default=False, is_flag=True, help="Prints the details")
def pvedit(filename, graph, verbose):
    '''
    Removes the silent part of a video file 
    '''
    ## Constants
    THRESHOLD = 0.15
    OUTER_MARGIN = 0.8
    INNER_MARGIN = 0.4

    clip = VideoFileClip(filename).fx(afx.audio_normalize)
    clip_audio = clip.audio.to_soundarray(fps=44100)
    sps = clip_audio.shape[0] / (clip.reader.nframes / clip.reader.fps)

    above_threshold_audio_pos = np.where(np.where(np.abs(clip_audio[:,0]) > THRESHOLD, True, False))[0]
    above_threshold_audio_pos_d = above_threshold_audio_pos[1:] - above_threshold_audio_pos[:-1]
    silent_audio_interval = np.where(above_threshold_audio_pos_d > 40000)[0]

    clip_new_total = 0

    clip_new_total = clip.subclip(
        above_threshold_audio_pos[0]/sps - OUTER_MARGIN, 
        above_threshold_audio_pos[silent_audio_interval[0]]/sps + INNER_MARGIN
    )

    for i in range(len(silent_audio_interval) - 1):
        clip_temp = clip.subclip(
            above_threshold_audio_pos[silent_audio_interval[i]+1]/sps - INNER_MARGIN,
            above_threshold_audio_pos[silent_audio_interval[i+1]]/sps + INNER_MARGIN
        )
        clip_new_total = concatenate_videoclips([clip_new_total,clip_temp])

    clip_temp = clip.subclip(
        above_threshold_audio_pos[silent_audio_interval[-1]+1]/sps - INNER_MARGIN,
        above_threshold_audio_pos[-1]/sps + OUTER_MARGIN
    )
    clip_new_total = concatenate_videoclips([clip_new_total,clip_temp])

    clip_new_total_audio=clip_new_total.audio.to_soundarray(fps=44100)
    # Export the new video
    clip_new_total.write_videofile(f"{filename[:-4]}-processed.mp4", threads=8, fps=30)
    
    if verbose:
        print("\n-------DETAILS-------\n")
        print(f"Time Reduction     - {(1 - len(clip_new_total_audio)/len(clip_audio)) * 100:.2f}%")
        print(f"Number of Cuts     - {len(silent_audio_interval)}")
        print(f"Sample per Seconds - {sps:0.0f}")
    
    if graph:
        #== PLOTTING ==
        plt.subplot(211)
        plt.plot(clip_audio, 'b', linewidth=0.5, label='Volume')
        plt.legend(loc="upper right", fontsize='small')
        plt.plot( np.ones(len(clip_audio)) * THRESHOLD,  'r', linewidth=0.5)
        plt.plot(-np.ones(len(clip_audio)) * THRESHOLD,  'r', linewidth=0.5)
        plt.subplot(212)
        plt.plot(clip_new_total_audio, 'b', linewidth=0.5, label='Volume')
        plt.legend(loc="upper right", fontsize='small')
        plt.show()

