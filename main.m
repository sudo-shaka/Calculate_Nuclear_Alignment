clear;

IMG = imread("Sample_Images/IMG.png");
IMG_MASK = imbinarize(IMG);

[CENTERS,RADII] = imfindcircles(IMG_MASK,[15 50],'Sensitivity',0.9);

NUCLEII = [];

for ii = 1:length(CENTERS)
	center = CENTERS(ii,:);
	overlapped = CENTERS(min((abs(center-CENTERS) < 2*RADII(ii))'),:);
	avg_overlapped = mean(overlapped);

	calculated = max(min(avg_overlapped' == reshape(NUCLEII,2,[])));

	if length(avg_overlapped) == 1
		NUCLEII = [NUCLEII,center];
	elseif ~calculated
		NUCLEII = [NUCLEII,center];
	end
end

NUCLEII = round(reshape(NUCLEII,2,[])');

len = length(NUCLEII);

fprintf("%d nucleii found.\n",len);

DATA = zeros(10,length(NUCLEII));
LENGTHS = zeros(2,length(NUCLEII));

for i = 1:length(NUCLEII)
	x1 = NUCLEII(i,1);
	y1 = NUCLEII(i,2);
	angles = [0,pi/2,pi,3*pi/2];
	DATA(1,i) = x1; DATA(2,i) = y1;
    
	for ii = 1:length(angles)
		pixel = 1;
		angle = angles(ii);
		x2 = x1; y2 = y1;
		while pixel
			try
				pixel = IMG_MASK(round(y2),round(x2));
				x2 = x2 + round(cos(angle));
				y2 = y2 + round(sin(angle));
			catch
				break;
			end
		end
		DATA(ii*2+1,i) = x2;
		DATA(ii*2+2,i) = y2;
	end

	LENGTHS(1,i) = DATA(3,i) - DATA(7,i);
	LENGTHS(2,i) = DATA(6,i) - DATA(10,i);
end

disp(LENGTHS(1,:)./LENGTHS(2,:));

