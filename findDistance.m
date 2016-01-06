function[Dis_to_obj] = findDistance(img)

foundSpirols = [];  %temporary sprilas 
distance = 0;
m = img;
centers = main_detect_spirals(m);       %get all spirals
                       
for i = 1:size(centers, 1)     %find the real spirals from all the spirals
    if centers(i, 3) < -0.85 && centers(i, 3) > -1.2      %for different angle of spirals add this condition with diffent angles in radian
        foundSpirols = cat(1,foundSpirols, centers(i, :));
    elseif centers(i, 3) < 0.99 && centers(i, 3) > 1.09
        foundSpirols = cat(1,foundSpirols, centers(i, :));
    end
end
        
if size(foundSpirols, 1) > 1     %calculate the distance between found real spirals
    distance = sqrt(((foundSpirols(2,1)-foundSpirols(1,1))^2)+((foundSpirols(2,2)-foundSpirols(1,2))^2));
    Dis_to_obj=(4.25*648.3492)/distance;  %for 320x280 =3.2, 640x480 = 5
    
else   %if no distance return big distance
    Dis_to_obj = 2;
end







   



