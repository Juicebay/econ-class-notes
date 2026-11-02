
% this program generates the transitional dynamics in the Solow-Swan growth model.

clear		%clear work space

% parameter calibration
alpha  = 1/3;					% capital's share parameter
x    	 = .02;					% Canada's average annual growth rate
delta  = .05;					% 5% annual depreciation rate
n      = .01;				    % population growth rate
s      = .25;				    % saving rate 
beta   = (1-alpha)*(delta+n+x); % convergence rate

% the steady state values
khatss = (s/(delta+n+x))^(1/(1-alpha));
yhatss = khatss^alpha;

% starting value
khat1  = .25*khatss;            

% Method A: calculate the transitional dynamics for khat and yhat by iterating on the fundamental differencial equation
khatdot    = zeros(100,1);      % create an empty matrix
khat       = zeros(100,1);
yhat       = zeros(100,1);
growth     = zeros(99,1);
khat(1)    = khat1;				 % initial value in the matrix
yhat(1)    = khat(1)^alpha;
khatdot(1) = s*yhat(1)-(delta+n+x)*khat(1);

for i=2:100						 % calculations for the remaining values
   khat(i)    = khatdot(i-1)+khat(i-1);
   yhat(i)    = khat(i)^alpha;
   khatdot(i) = s*yhat(i)-(delta+n+x)*khat(i);
   growth(i-1)= log(yhat(i))-log(yhat(i-1));
end

% Method B: calculate the transitional dynamics for khat and yhat using the closed form analytical solution derived in class
khat2       = zeros(100,1);
yhat2       = zeros(100,1);
growth2     = zeros(99,1);
khat2(1)    = khat1;

for j=1:100
   khat2(j)    = (khatss^(1-alpha)+(khat2(1)^(1-alpha)-khatss^(1-alpha))*exp(-(1-alpha)*(delta+n+x)*(j-1)))^(1/(1-alpha));
   yhat2(j)    = khat2(j)^alpha;
end

for j=2:100
   growth2(j-1)= log(yhat2(j))-log(yhat2(j-1));
end

% Method C: calculate the transitional dynamics for khat and yhat using the log-linearized solution derived in class

khat3       = zeros(100,1);
yhat3       = zeros(100,1);
growth3     = zeros(99,1);
khat3(1)    = khat1;

for k=1:100
   khat3(k)    = exp(log(khatss)-(log(khatss)-log(khat3(1)))*exp(-(1-alpha)*(delta+n+x)*(k-1)));
   yhat3(k)    = khat3(k)^alpha;
end

for j=2:100
   growth3(j-1)= log(yhat3(j))-log(yhat3(j-1));
end

%compare the simulations from the various solution methods
compare=[growth,growth2,growth3];
plot(compare)

