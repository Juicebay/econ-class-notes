% ECON*6020 Assignment 2, parts (f) and (g): Arrow learning-by-investing.
% Xingming Li, ID 1432037

clear		%clear work space

% parameter calibration
alpha  = 1/3;					% capital's share parameter
a      = 1;					    % technology scale parameter
delta  = .10;					% 10% annual depreciation rate
LN     = 1;				        % workers per firm, L/N
s      = .25;				    % saving rate
T      = 100;                   % number of years to simulate

% the steady state values for b=0
b      = 0;
kss    = (s*a^(1-alpha)*LN^(b*(1-alpha))/delta)^(1/((1-alpha)*(1-b)));
yss    = a^(1-alpha)*LN^(b*(1-alpha))*kss^(b*(1-alpha)+alpha);

% starting value (the same for both experiments)
k1     = .25*kss;

% Method C: calculate the transitional dynamics for k and y using the log-linearized solution
%   log k(t) = log kss - (log kss - log k(1))*exp(-beta*(t-1)),  beta = (1-alpha)*(1-b)*delta
bvals  = [0, 1/2];
growth = zeros(T,2);
kpath  = zeros(T+1,2);
ypath  = zeros(T+1,2);

for m=1:2
   b       = bvals(m);
   kssb    = (s*a^(1-alpha)*LN^(b*(1-alpha))/delta)^(1/((1-alpha)*(1-b)));   % steady state for this b
   beta    = (1-alpha)*(1-b)*delta;                                          % convergence rate
   k       = zeros(T+1,1);      % create an empty matrix
   y       = zeros(T+1,1);
   k(1)    = k1;				 % initial value in the matrix

   for j=1:T+1
      k(j)  = exp(log(kssb)-(log(kssb)-log(k(1)))*exp(-beta*(j-1)));
      y(j)  = a^(1-alpha)*LN^(b*(1-alpha))*k(j)^(b*(1-alpha)+alpha);
   end

   for j=2:T+1
      growth(j-1,m) = log(y(j))-log(y(j-1));
   end
   kpath(:,m) = k;
   ypath(:,m) = y;
end

% steady state for b=1/2 
kss_half = (s*a^(1-alpha)*LN^(.5*(1-alpha))/delta)^(1/((1-alpha)*(1-.5)));

fprintf('b=0:   kss = %.4f, yss = %.4f, k1 = %.4f\n', kss, yss, k1);
fprintf('b=1/2: kss = %.4f\n', kss_half);
for t=[1 2 5 10 20 30 50 100]
   fprintf('year %3d: growth b=0 = %6.3f%%, growth b=1/2 = %6.3f%%\n', t, 100*growth(t,1), 100*growth(t,2));
end

%compare the two simulated growth paths
years = (1:T)';
plot(years,100*growth(:,1),'b-',years,100*growth(:,2),'r--','LineWidth',1.5)
xlabel('Year')
ylabel('Growth rate of income per capita (%)')
legend('b = 0','b = 1/2')
title('Growth of income per capita, k(0) = k^*(b=0)/4')
grid on
print('-dpng','hw2_f_growth.png')

% Part (g): Golden Rule for b=0, maximize c = y - delta*k  ->  alpha*a^(1-alpha)*k^(alpha-1) = delta
kgold = (alpha*a^(1-alpha)/delta)^(1/(1-alpha));
sgold = delta*kgold/(a^(1-alpha)*kgold^alpha);    % equals alpha
fprintf('Golden Rule: kgold = %.4f, sgold = %.4f, kss(s=0.25) = %.4f\n', kgold, sgold, kss);
if s < sgold
   fprintf('s < sgold, so kss < kgold: dynamically efficient.\n');
else
   fprintf('s > sgold: dynamically inefficient.\n');
end
