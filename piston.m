function [P] = piston( f, a_h, a_v, theta, phi )
%[P] = piston( f, a_h, a_v, theta, phi )
%
% Rigid elliptical piston in an infinite baffle,
% at frequency f Hz,
% with horizontal radius a_h (in meters) and vertical radius a_v.
%
% following description in the book by Beranek, Leo L. (1954). Acoustics.
% (yes, there is a more recent edition, but I % don't have a copy...)
%
% Theta and phi, which are azimuth and elevation, resp., have units of
% radians.  P is sound pressure in units of N/m^2 (? this should be
% verified). If theta and phi are scalars, or one is a vector, then
% behavior is as you would expect: you get a scalar or vector back.
%
% If both theta and phi are vectors, then P is a matrix where where
% columns correspond to values of theta, and rows correspond to values
% of phi.
%
% NOTES: - It is possible I have made a mistake in the below
%          computations. The returned values from besselj are complex
%          with, in some places, small but nonzero imaginary
%          components.  I address this by taking absolute value of P
%          (i.e. complex magnitude); this matches intuition but awaits
%          confirmation till I learn more acoustics theory
%
%
% Scott Livingston  <slivingston@caltech.edu>
% 23 Jan 2011.

c = 343; % m/s speed of sound (assumed)
k = 2*pi*f/c; % thus get wave number

h_term = k*a_h*sin(theta);
v_term = k*a_v*sin(phi);

if size(h_term,1) > size(h_term,2) % force to be row vector?
    h_term = h_term';
end
if size(v_term,2) > size(v_term,1) % force to be columnvector?
    v_term = v_term';
end

h_factor = ones(size(h_term));
I = find(h_term ~= 0);
h_factor(I) = besselj(1,h_term(I))./h_term(I);

v_factor = ones(size(v_term));
I = find(v_term ~= 0);
v_factor(I) = besselj(1,v_term(I))./v_term(I);

P = 4*abs(v_factor*h_factor); % make P from outer product.
