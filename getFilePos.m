function [start, stop] = getFilePos(file_start, event_start, event_stop, buffer, sampleRate)
start_samp = (event_start(1)*3600 + event_start(2)*60 + event_start(3) - buffer)*sampleRate;
stop_samp = (event_stop(1)*3600 + event_stop(2)*60 + event_stop(3) + buffer)*sampleRate;
file_start_samp = (file_start(1)*3600 + file_start(2)*60 + file_start(3))*sampleRate;
start = mod((start_samp - file_start_samp), (24*60*60*sampleRate));
stop = mod((stop_samp - file_start_samp), (24*60*60*sampleRate));