clear all
disp('its here')
% ip = client ip 

t = tcpip('192.168.0.100', 9092, 'NetworkRole', 'server', 'InputBufferSize', 61440);
fopen(t)
disp('Client connected...')
i = 1;
k = 1;
srr= [];
finn = [];
A = [];
foundSpirols = [];
d = 0;
while(1)
    while (t.BytesAvailable > 0)
        A = cat(1,A,fread(t, t.BytesAvailable));
    end
    if(size(A, 1) == 307200)
        img = reshape(A,[640, 480]);
        I = mat2gray(img);
        I = imrotate(I,270);
        I = flipdim(I ,2);
        imshow(I);
        centers = fun_4_cv_tcp(I);
        srr{i} = centers;
        j = 0;
        for i = 1:size(centers, 1)
            if centers(i, 3) > 0.99 & centers(i, 3) < 1.09
                foundSpirols = cat(1,foundSpirols, centers(i, :));
            elseif centers(i, 3) < 0.99 & centers(i, 3) > 1.09
                foundSpirols = cat(1,foundSpirols, centers(i, :));
            end
        end
        if size(foundSpirols,1)
            finn{k} = foundSpirols;
            k = k + 1;
       
        end
        if size(foundSpirols, 1) > 1
            disaa = [foundSpirols(1,1), foundSpirols(2,1)
            foundSpirols(1,2), foundSpirols(2,2)];
            d = pdist(disaa,'euclidean');
        end
        d
        foundSpiros = [];
        A = [];
        i = i + 1;
        fwrite(t, '1')
    end
end

fclose(u)
delete(t)
clear t
