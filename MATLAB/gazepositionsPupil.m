% Recording number 2017-06-19-001

N = csvread('pupil_postions.csv', 1);

timestamp = N(:,1);
norm_pos_x = N(:,5); % norm_pos_x
norm_pos_y = N(:,6); % norm_pos_y

% simple moving average 
window_size = 12; 
mv_norm_x = tsmovavg(norm_pos_x,'s',window_size, 1);
mv_norm_y = tsmovavg(norm_pos_y,'s',window_size, 1);


timestamp(end,1)

i = 1;
n = timestamp(i,1);

while(n < timestamp(end))

      t(i) = rand(1);
      i=i+1;
      set(gcf,'color','white');
      drawnow;
      plot(norm_pos_x(i,1), norm_pos_y(i,1),'-.dk','linewidth',1.8)
      axis([-1 1 -1 1])
      grid off;
      title('Pupil gaze in Image Plane');
      xlabel('norm pos x');
      ylabel('norm pos y');
      %pause(0.5);

end

% while(n < timestamp(end))
% 
%       t(i) = rand(1);
%       i=i+1;
%       set(gcf,'color','white');
%       drawnow;
%       plot(norm_x(i,1), norm_pos_y(i,1),'-.dk','linewidth',1.8)
%       axis([-1 1 -1 1])
%       grid off;
%       title('Pupil gaze in Image Plane');
%       xlabel('norm pos x');
%       ylabel('norm pos y');
%       n = timestamp(i,1);
%       %pause(0.5);
% 
% end
