% ECON*6020 Assignment 3: calibration and transitional dynamics of the Ramsey model.
% Xingming Li, ID 1432037

clear		%clear work space
close all

% parameter calibration (Canadian long-run averages)
alpha  = 1/3;					% capital's share of income (labour share = 2/3)
x      = .02;					% growth rate of income per capita
delta  = .05;					% 5% annual depreciation rate
n      = .01;				    % population growth rate
rho    = .01;				    % rate of time preference, exp(-rho) = 0.99
s_data = .25;				    % investment-GDP ratio
A0     = 1;                     % initial productivity level, A(0)=1
T      = 100;                   % number of years to simulate
dt     = .01;                   % step size for the numerical integration

% Part (1): calibrate theta from the steady-state saving rate
%   s_ss = alpha*(delta+n+x)/(delta+rho+theta*x)  ->  solve for theta
theta  = (alpha*(delta+n+x)/s_data - delta - rho)/x;
r_ss   = delta + rho + theta*x;                 % rental rate = alpha*khat^(alpha-1)
fprintf('Part (1): theta = %.4f\n', theta);
fprintf('          rental rate r = %.4f, net interest rate r - delta = %.4f\n', r_ss, r_ss-delta);
fprintf('          check: rho - n - (1-theta)x = %.4f > 0\n', rho-n-(1-theta)*x);

% Parts (2)-(4): transitional dynamics for each value of theta
%   cdot/c = (alpha*k^(alpha-1) - delta - rho - theta*x)/theta
%   kdot   = k^alpha - (delta+n+x)*k - c
% The saddle path is found by "reverse shooting": start next to the steady state on the
% stable eigenvector and integrate the system backward in time. This traces out c as a
% function of k along the saddle path. We then simulate forward from k(0) = kss/4.
thetas = [theta, 9, 20];
years  = (0:T)';
spath  = zeros(T+1,3);          % saving rate
ypath  = zeros(T+1,3);          % income per person, y = A*khat^alpha
kpath  = zeros(T+1,3);
beta   = zeros(1,3);            % speed of convergence

for m=1:3
   th    = thetas(m);
   kss   = (alpha/(delta+rho+th*x))^(1/(1-alpha));      % steady state for this theta
   css   = kss^alpha - (delta+n+x)*kss;
   kdot  = @(k,c) k.^alpha - (delta+n+x)*k - c;
   cdot  = @(k,c) c.*(alpha*k.^(alpha-1) - delta - rho - th*x)/th;

   % Jacobian at the steady state and the stable eigenvalue (part 3)
   J     = [alpha*kss^(alpha-1)-(delta+n+x), -1;
            css*alpha*(alpha-1)*kss^(alpha-2)/th, 0];
   [V,D] = eig(J);
   [lam,i] = min(diag(D));                               % negative eigenvalue
   beta(m) = -lam;
   v     = V(:,i)/V(1,i);                                % stable direction, normalized dk=1

   % reverse shooting: integrate backward (RK4 with step -dt) from near the steady state
   k0    = .25*kss;              % starting value: 1/4 of the steady state for this theta
   kb    = kss*(1-1e-6);
   cb    = css + v(2)*(kb-kss);
   K     = kb;  C = cb;
   while kb > .9*k0
      k1 = kdot(kb,cb);                 c1 = cdot(kb,cb);
      k2 = kdot(kb-dt/2*k1,cb-dt/2*c1); c2 = cdot(kb-dt/2*k1,cb-dt/2*c1);
      k3 = kdot(kb-dt/2*k2,cb-dt/2*c2); c3 = cdot(kb-dt/2*k2,cb-dt/2*c2);
      k4 = kdot(kb-dt*k3,cb-dt*c3);     c4 = cdot(kb-dt*k3,cb-dt*c3);
      kb = kb - dt/6*(k1+2*k2+2*k3+k4);
      cb = cb - dt/6*(c1+2*c2+2*c3+c4);
      K(end+1,1) = kb;  C(end+1,1) = cb;  %#ok<SAGROW>
   end
   K  = [flipud(K); kss];  C = [flipud(C); css];          % saddle path c(k), k increasing
   cpol = @(k) interp1(K,C,min(k,kss),'pchip');

   % forward simulation along the saddle path, recorded once a year
   k  = zeros(T+1,1);
   k(1) = k0;
   kt = k0;
   for j=2:T+1
      for h=1:round(1/dt)
         f1 = kdot(kt,cpol(kt));
         f2 = kdot(kt+dt/2*f1,cpol(kt+dt/2*f1));
         f3 = kdot(kt+dt/2*f2,cpol(kt+dt/2*f2));
         f4 = kdot(kt+dt*f3,cpol(kt+dt*f3));
         kt = kt + dt/6*(f1+2*f2+2*f3+f4);
      end
      k(j) = kt;
   end
   c  = cpol(k);
   yh = k.^alpha;                                         % income per effective worker
   kpath(:,m) = k;
   spath(:,m) = 1 - c./yh;                                % saving rate s = 1 - c/y
   ypath(:,m) = A0*exp(x*years).*yh;                      % income per person

   fprintf('\ntheta = %5.2f: kss = %.4f, css = %.4f, s_ss = %.4f, 1/theta = %.4f\n', ...
           th, kss, css, alpha*(delta+n+x)/(delta+rho+th*x), 1/th);
   fprintf('              speed of convergence beta = %.4f\n', beta(m));
   for t=[0 1 5 10 20 30 50 100]
      fprintf('   year %3d: s = %.4f\n', t, spath(t+1,m));
   end
end

% growth rate of income per person in the benchmark case
growth = diff(log(ypath(:,1)));
fprintf('\nPart (2): growth rate of income per person (theta = %.4f)\n', theta);
for t=[1 2 5 10 20 30 50 100]
   fprintf('   year %3d: %.3f%%\n', t, 100*growth(t));
end

% Part (3): compare with the Solow model at s = 0.25
beta_solow = (1-alpha)*(delta+n+x);
fprintf('\nPart (3): Ramsey beta = %.4f, Solow beta = %.4f\n', beta(1), beta_solow);
% formula from the log-linearization: 2*beta = sqrt(zeta^2 + 4*(1-alpha)/theta*(rho+delta+theta*x)*[(rho+delta+theta*x)/alpha - (n+x+delta)]) - zeta
zeta  = rho - n - (1-theta)*x;
beta_f = (sqrt(zeta^2 + 4*(1-alpha)/theta*(rho+delta+theta*x)*((rho+delta+theta*x)/alpha-(n+x+delta))) - zeta)/2;
fprintf('          closed-form beta = %.4f\n', beta_f);

% Part (2) figures
figure(1)
plot(years,100*spath(:,1),'b-','LineWidth',1.5)
xlabel('Year')
ylabel('Saving rate (%)')
title(sprintf('Saving rate, \\theta = %.2f, k(0) = k^*/4', theta))
grid on
print('-dpng','hw3_saving.png')

figure(2)
plot(years,ypath(:,1),'b-','LineWidth',1.5)
xlabel('Year')
ylabel('Income per person, y = A\cdot k^{\alpha}')
title(sprintf('Income per person, \\theta = %.2f, k(0) = k^*/4', theta))
grid on
print('-dpng','hw3_income.png')

figure(3)
plot(years(2:end),100*growth,'b-','LineWidth',1.5)
hold on
plot(years(2:end),100*x*ones(T,1),'k:')
hold off
xlabel('Year')
ylabel('Growth rate of income per person (%)')
title(sprintf('Growth of income per person, \\theta = %.2f', theta))
grid on
print('-dpng','hw3_growth.png')

% Part (4) figure: saving rates for the three values of theta
figure(4)
plot(years,100*spath(:,1),'b-',years,100*spath(:,2),'r--',years,100*spath(:,3),'k-.','LineWidth',1.5)
xlabel('Year')
ylabel('Saving rate (%)')
legend(sprintf('\\theta = %.2f',theta),'\theta = 9','\theta = 20','Location','east')
title('Saving rate, k(0) = k^*(\theta)/4')
grid on
print('-dpng','hw3_saving_theta.png')
