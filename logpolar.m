function logpolar( fig_handle, Theta, R )
%logpolar( fig_handle, Theta, R )
%
% R radius is presented in log scale normalized (w.r.t. its maximum
% value). The origin corresponds to -\infty (i.e. R going to zero) and
% the maximum R value is mapped to 1.
%
% Theta is shifted by +\pi/2 radians to make 0 angle ``pointing up.''
%
%
% Scott Livingston  <slivingston@caltech.edu>
% 23 Jan 2011.

lR = log(abs(R)/max(abs(R)));
figure(fig_handle)
polar(Theta+pi/2, (lR-min(lR))/abs(max(lR-min(lR))),'bo-')
