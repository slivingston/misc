function f = estfreq( t, x, thr, t_win )
%function f = estfreq( t, x, thr=0, t_win=[t(1),t(end)] )
%
% x - data vector (waveform)
% t - time vector corresponding to x; we assume length(x) == length(t)
% thr - threshold about which to count crossings and thus by which
%       to estimate frequency;
%       default value is 0 (i.e. "zero crossings").
% t_win - time window to consider.
%
%
% Scott Livingston  <slivingston@caltech.edu>
% 23 April 2010.


% Handle function arguments
if nargin < 2 || isempty(t) || isempty(x)
    f = -1;
    return
end
if nargin < 4
    t_win = [t(1) t(end)];
end
if nargin < 3
    thr = 0;
end

xl = [min(find(t >= t_win(1))) max(find(t <= t_win(2)))];

x_above = x(x(xl(1):xl(2)) >= thr);
x_below = x(x(xl(1):xl(2)) < thr);

if isempty(x_above) || isempty(x_below)
   fprintf('Error: insufficiently many crossings.\n');
   f = -1;
   return
end

I = find(x(xl(1):xl(2)) >= thr);
dI = find(diff(I)>1);
f = 1/mean(diff(t(I(dI)+xl(1)-1)));
