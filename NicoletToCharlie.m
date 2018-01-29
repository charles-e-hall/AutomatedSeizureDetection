function NicoletToCharlie(path, file)
    %I am very limited in terms of the available RAM that I have
    %in my machines, so I am attempting to do this conversion in a way that
    %hopefully doesn't use up all of the RAM that I have and crash
    %my computer.
    %This script takes Nicolet files and converts them to 
    %a binary file format that I made up which is convenient
    %for my purposes.

    obj = NicoletFile([path file]);
    blockSize = obj.segments.samplingRate(1)*obj.segments.duration;
    chunk = obj.segments.samplingRate(1)*obj.segments.duration / 2;
    fname_parts = strsplit(file, '.');
    fname_out = strcat(fname_parts(1), '.ceh');
    fo = fopen(char(strcat(path, fname_out)), 'a');
    %Original File Name field is 40 bytes (assuming 8 byte encoding)
    header = [sprintf('%-40s', file) sprintf('%-100s', path) ...
        sprintf('%04d', obj.segments.startDate(1)) sprintf('%02d', obj.segments.startDate(2)) ...
        sprintf('%02d', obj.segments.startDate(3)) sprintf('%02d', obj.segments.startTime(1)) ...
        sprintf('%02d', obj.segments.startDate(2)) sprintf('%02d', obj.segments.startTime(3))];
    
    fwrite(fo, header);
    fwrite(fo, obj.segments.samplingRate(1), 'uint32');
    fwrite(fo, obj.segments.duration, 'uint32');
    fbase = 162;
    
    for i=1:27
       chName = sprintf('%-4s', char(obj.segments.chName(i)));
       fwrite(fo, chName);
       pointer = fbase + blockSize*i;
       fwrite(fo, pointer, 'uint64');
    end
    
    for j=1:27
        out = getdata(obj, 1, [1 chunk], j);
        fwrite(fo, out, 'double', 'ieee-le');
        out = getdata(obj, 1, [chunk+1 blockSize], j);
        fwrite(fo, out, 'double', 'ieee-le');
    end
        