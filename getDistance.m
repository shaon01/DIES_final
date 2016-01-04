function [dist] = getDistance(img)
%imrgb=imread('two_pies_different_freq.jpg');

%imrgb=imread('spirals20.jpg');
imrgb=img;
dimensions=size(imrgb);

%1. roi is the full image
mrect =     [1    1   size(imrgb,2) size(imrgb,1)]; thresh=0.8;%entire image as rectangle... ideal thresh around 0.6

%Region Of Interest, roi, is in the order: rowTL,colTL,rowBR, colBR 
%Translate matlab rectangle to roi
roi=mrect;
botr=roi(1:2)+roi(3:4)-1;
roi=[roi(1:2),botr];
roi=[roi(2),roi(1),roi(4),roi(3)];
roi_imrgb=imrgb(roi(1):roi(3),roi(2):roi(4),:);
roi_im=roi_imrgb(:,:,2);
%figure(1);imshow(roi_imrgb ); truesize

%Initialization: produce centroid masks (rowmask and colmask)
 Ncm=15; Nch=(Ncm-1)/2;
 colmask=ones(Ncm,1)*[-Nch:Nch]; % rowmask=reshape(rowmask, [Ncm*Ncm,1]);rowmask=rowmask';
 rowmask=[-Nch:Nch]'*ones(1,Ncm); %colmask=reshape(colmask, [Ncm*Ncm,1]);colmask=colmask';


%initialization: spiral detection
%generate 4 1D derivative filters and a 2D complex filter.
sma1=(0.75); %0.75  
dx=gaussgen(sma1,'dxg',[1,round(sma1*6)]);
gx=gaussgen(sma1,'gau',[1,round(sma1*6)]);
dy=-dx';
gy=gx';

sma2=(16); 
sma=[sma1,sma2];
typ=2; sm=double(-sma2); gammaf=100;
% ...if sm is negative then symdergaussgen interprets it as the radius
%   that we wish that the max filter values will occur (instead of standard
%   deviation.
h2=symdergaussgen(typ,sm,gammaf);
%            [i,j,s] = find(h2);
%                [m,n] = size(h2);
%                h2 = sparse(i,j,s,m,n);
scaling=['sclon'];
gamma=0.01;
%Info=['....ENTERING ROI COMPUTATIONS....ENTERING ROI COMPUTATIONS....ENTERING ROI COMPUTATIONS...']

ptime=[];
tic;
%DETECT spiral objects. 
[spiral_obj_roi,I20nmxs,I20]=spiral_detection_buf(double(roi_im),sma,scaling,gamma,dx,gx,dy,gy,h2,rowmask,colmask,thresh);
spiral_obj=[];
if size(spiral_obj_roi,1)>0 
spiral_obj=[roi(1)+spiral_obj_roi(:,1)-1,roi(2)+spiral_obj_roi(:,2)-1,spiral_obj_roi(:,3)];
end
ptime=[ptime toc];

if size(spiral_obj_roi,1)>0 
imrgb(:,:,2)=mark_obj(imrgb(:,:,2),spiral_obj);

%store coordinates of spirals center
coordinates=round(spiral_obj(:,1:2));

%Number of spiral objects 
%[centers, radii] = imfindcircles(spiral_obj)
Number_of_spiral_obj=size(spiral_obj,1)
end

ptime=[ptime sum(ptime) ptime/sum(ptime)];

%
%same==> times we find same distances between consecutive points
same=0;
%real distance=average distance between 3 consecutive points:A,B,C====> (AB+BC)/2
realdistance=0;
%distance_between_centers!
distance=[];
if Number_of_spiral_obj>=3 & Number_of_spiral_obj<=6
%change columns of matrix (first columns x-axis)
coordinates(:,[1,2])=coordinates(:,[2,1]);
%sort matrix based on x axis (columns)
sorted=sortrows(coordinates);
%find points x-coordinate of each spiral
points=size(coordinates,1);
%calculate distance between 2centers with formula
%d=sqr[(x2-x1)^2+(y2-y1)^2]  and check if distances between 3 points is same
for i=1:1:points-1
    distance(i)=sqrt(((sorted(i+1,1)-sorted(i,1))^2)+((sorted(i+1,2)-sorted(i,2))^2));
    if (i>=2)
        if abs(int16(distance(i))-int16(distance(i-1)))<=15
            same=same+1;
            if same>=1
                realdistance=(distance(i)+distance(i-1))/2;
                colors=spiral_obj(i-1:i+1,3);
                %DistanceToObject=(W*F)/P
                DistanceToObject=(5*648.3492)/realdistance;
            end
        end
    end
end
%decode colors to identity 0 and 1
for j=1:size(colors,1)
    if colors(j)>0 & colors(j)<1.5
        identity(j)=1;
    elseif colors(j)<0 & colors(j)>-1.5
        identity(j)=0;
    end
end
%colors
%realdistance
identity;
dist = DistanceToObject;
elseif Number_of_spiral_obj<3
    disp('No spirals Detected Decrease Threshold')
elseif Number_of_spiral_obj>6
    disp('Too many spirals Detected Increase Threshold')
end
%RealDistance=(SizeSpacemm*FocalLenght)/realdistancePixels
%Focal length	3.60 mm +/- 0.01
%%End: Info