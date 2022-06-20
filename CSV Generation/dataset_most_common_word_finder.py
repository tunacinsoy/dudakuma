from __future__ import unicode_literals
import sys
import os.path
import re
import glob
import string

### this script will analyze all subtitles(.vtt files) and give most common words in corpus of subtitles
### make sure all subtitles(.vtt files) are o the same working directory as with this script

def main(argv):
    all_word_list = []
    for file in glob.glob("VTT_FILES_PATH/*.vtt"):
        # subtitle has been downloaded succesfully
        ##### PROCESSING SUBTITLE FILE PART #####
        caption_list = []
        file1 = open(file, 'r',encoding="utf-8") 
        sbt_lines = file1.readlines()
        file1.close()
        vtt_pattern = re.compile("(?m)^(\d{2}:\d{2}:\d{2}\.\d+) +--> +(\d{2}:\d{2}:\d{2}\.\d+)")
        found_vtt_timestamp = False
        vtt_timestamp_start = None
        vtt_timestamp_end = None
        for line in sbt_lines:
            if found_vtt_timestamp:
                found_vtt_timestamp = False
                caption = {
                "start": vtt_timestamp_start,
                "end": vtt_timestamp_end,
                "text": line
                }
                if len(line.strip()) == 0:
                    continue
                caption_list.append(caption)
                continue
            
            result = vtt_pattern.match(line)
            if result:
                found_vtt_timestamp = True
                vtt_timestamp_start = result.group(1)
                vtt_timestamp_end = result.group(2)
            else:
                continue

        for c in caption_list:
            sentence = c['text']
            sentence = sentence.lstrip().lower()
            translator = str.maketrans(string.punctuation, ' '*len(string.punctuation)) #map punctuation to space
            cleaned_sentence = sentence.translate(translator)

            for eachword in cleaned_sentence.split():
                all_word_list.append(eachword)

    from collections import Counter
    all_counter = Counter(all_word_list)
    mcw = all_counter.most_common(1000)
    for m in mcw:
        print(m)
    print("Total word count: " + str(len(all_word_list)))
    print("Total unique word count: " + str(len(all_counter.keys())))

    
if __name__ == "__main__":
    main(sys.argv)
