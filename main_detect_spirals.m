function[spirals] = main_detect_spirals(img)
    
    imrgb = img;
    mrect =     [1    1   size(imrgb,2) size(imrgb,1)]; thresh=0.6;%defalut 0.6 %entire image as rectangle...
    
    %Region Of Interest, roi, is in the order: rowTL,colTL,rowBR, colBR
    %Translate matlab rectangle to roi
    roi=mrect;
    botr=roi(1:2)+roi(3:4)-1;
    roi=[roi(1:2),botr];
    roi=[roi(2),roi(1),roi(4),roi(3)];
    roi_imrgb=imrgb(roi(1):roi(3),roi(2):roi(4),:);
    roi_im=roi_imrgb(:,:,2);
    %figure(21);imshow(roi_imrgb ); truesize
    
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
    
    sma2=(16); %defalult 16
    sma=[sma1,sma2];
    typ=2; sm=double(-sma2); gammaf=100;
    % ...if sm is negative then symdergaussgen interprets it as the radius
    %   that we wish that the max filter values will occur (instead of standard
    %   deviation.
    h2=symdergaussgen(typ,sm,gammaf);
    scaling=['sclon'];
    gamma=0.01;
    
    ptime=[];
    tic
    %DETECT spiral objects.
    [spiral_obj_roi,I20nmxs,I20]=spiral_detection_buf(double(roi_im),sma,scaling,gamma,dx,gx,dy,gy,h2,rowmask,colmask,thresh);
    spiral_obj=[];
    if size(spiral_obj_roi,1)>0
        spiral_obj=[roi(1)+spiral_obj_roi(:,1)-1,roi(2)+spiral_obj_roi(:,2)-1,spiral_obj_roi(:,3)];
    end
    ptime=[ptime toc];
    
    if size(spiral_obj_roi,1)>0
        imrgb(:,:,2)=mark_obj(imrgb(:,:,2),spiral_obj);
        spiral_obj;
        
    end
    %figure(5);imshow(imrgb); axis image; truesize    
    ptime=[ptime sum(ptime) ptime/sum(ptime)];
    spirals = spiral_obj;  %returning all the spirals
    
   
