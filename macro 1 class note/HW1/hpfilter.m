clear                                 % clears memory

a = load ('data2026q2.csv');	        %  hpdata=[y,c,i,gc,gi,ex,im,nx,n,w,k,mpk,exrate,pgdp, cpi,r,1+r]
										                  %  1976Q1-2026Q2

lambda =1600;
[T,nvar]=size(a);   					        % nvar = # of variables, T = # of periods (202 quarters)

d = (1+6*lambda)*ones(T,1);
x = diag(d);
d = -4*lambda*ones(T-1,1);
x = x + diag(d,1) + diag(d,-1);
d = lambda*ones(T-2,1);
x = x + diag(d,2) + diag(d,-2);
x(1,1) = 1+lambda;
x(1,2) = -2*lambda;
x(2,1) = -2*lambda;
x(2,2) = 1+5*lambda;
x(T,T) = 1+lambda;
x(T-1,T) = -2*lambda;
x(T,T-1) = -2*lambda;
x(T-1,T-1) = 1+5*lambda;
hpmat = inv(x);								    % matrix to apply HP filter
raw = log(a);								      % raw is logged data series
hptrend = hpmat*raw;						  % calculate HP trend line
hpdata = raw-hptrend; 						% deviation from HP trend
vcv = (hpdata'*hpdata)/T;					% variance-covariance matrix
var = sum(vcv .* eye(nvar,nvar)); % variance (vector)
sd = sqrt(var)*100;							  % std.dev (vector)
corr = vcv ./ sqrt(var'*var);			% corr (matrix)

% calculation autocorr for output. This provides a measure of persistence.
yhp = hpdata(2:T,1);              % for periods 2:T
yhplag = hpdata(1:T-1,1);         % for periods 1:T-1
autoy = corrcoef(yhp, yhplag);
