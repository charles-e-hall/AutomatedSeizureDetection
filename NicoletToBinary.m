function NicoletToBinary(source_path, dest_path, start, stop, buffer, channel)
obj = NicoletFile(source_path);
assert(length(start)==3, 'start must be a 3 element vector');
assert(length(stop)==3, 'stop must be a 3 element vector');
start = cell2mat(start);
stop = cell2mat(stop);
channel = uint8(channel);
fprintf('%u', channel);
fprintf('\n');

[seg_start, seg_stop] = getFilePos(obj.segments(1).startTime, start, stop, buffer, obj.segments(1).samplingRate(1));

try
    out = getdata(obj, 1, [seg_start seg_stop], 1:27);
catch
    if (seg_stop - seg_start) >= 100000
        out = zeros(1000, 27);
        fprintf('Had to write all zeros\n');
    else
        out = zeros((seg_stop - seg_start), 27);
        fprintf('Had to write all zeros\n');
    end
end    
%pre-allocate data
% data = zeros(size(out));
% if filter
%     [b, a] = butter(5, 0.2);
%     for i=1:27
%         data(:,i) = filter(b, a, out(:,i));
%     end
% else
%     data = out;
% end    
data = out.*obj.segments(1).scale(1);    

fh = fopen(dest_path, 'a', 'ieee-le');

%Write header information (Number of samples per channel)
totSamps = seg_stop - seg_start;
fwrite(fh, totSamps, 'uint64', 'ieee-le');
fwrite(fh, channel, 'uint8', 'ieee-le');

fwrite(fh, data, 'float', 'ieee-le');

fclose(fh);