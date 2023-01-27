import music21
import music21.features as features
from music21 import midi
from music21 import stream
from helper_functions import *
from numpy.random import randint

import numpy as np

from collections import namedtuple

from numpy.random import Generator, PCG64
rng = Generator(PCG64(9))


# function to extract n streams, target duration T seconds for composer 

# extracts n_clips each from n_tracks

# will use namedtuples as convient way to store clips, composer info

Clip = namedtuple('Clip',['composer','path','start','stop','seconds','stream'])

def extract_samples(audio_path_list,T=15,n_clips=1,show_streams=False):
    delta_measures = list(range(5,50,1))

    clips = []
    
    for audio_path in audio_path_list:
        
        print(audio_path)
        
        mf = midi.MidiFile()
        mf.open(audio_path) # path='abc.midi'
        mf.read()
        mf.close()
        s = midi.translate.midiFileToStream(mf)

        total_time = s.secondsMap[0]['durationSeconds']

        number_of_measures = len(s[0])  # think this is total number of measures in the stream?

        #print(audio_path,'lasts approx ',total_time,' seconds')
        
        #pick n_clips random measures to start clipping from 
        
        #start_measures = randint(1,number_of_measures//2,size=n_clips)
        start_measures = rng.integers(1,number_of_measures//2,size=n_clips)
        
        for i,start in enumerate(start_measures):
            
            for delta in delta_measures:

                stop = start+delta

                excerpt_stream = s.measures(start,stop)

                clip_time = excerpt_stream.secondsMap[0]['durationSeconds']

                if clip_time>T: # clip sample streams until time is longer than T
                    print('clip: ',i,' --> ','t = ',clip_time,'start = ',start,'stop =',stop,' delta = ',delta)

                    #clip = (composer,audio_path,start,stop,clip_time,excerpt_stream)
                    
                    clip = Clip(composer='UNKNOWN',
                                path=audio_path,
                                start=start,
                                stop=stop,
                                seconds=clip_time,
                                stream = excerpt_stream)
                    
                    clips.append(clip)
                    
                    if show_streams: excerpt_stream.show('midi')
                        
                    break                 
    
    return clips

def essential_features_from_stream(s,features_list,output=False):
    
    feature_values_vector = []
    
    for name in features_list: 
        
        extractor = getattr(features.jSymbolic,name+'Feature') 

        fe = extractor(s)
        
        val = fe.extract().vector
        
        feature_values_vector.append(val[0])
        
        if output: print(f'{name} {val}')
            
    return feature_values_vector


import re

def extract_data(clips,features_list):
    
    print(f"Beginning Feature Extraction for {len(clips)} clips")
    
    vectors = []
    
    clip_id_codes = []
    
    for i in range(len(clips)):
        
        print(f"extracting clip {(i+1)}/{len(clips)}...")
        #feature_vector = features_from_stream(clips[i].stream,output=False)
        
        feature_vector = essential_features_from_stream(clips[i].stream,features_list,output=False)
        
        path = clips[i].path
        
        code = re.findall(r'(0.\d+)_',path)[0]
        
        vectors.append(feature_vector)
        
        clip_id_codes.append(code)
        
    return clip_id_codes, np.vstack(vectors)









